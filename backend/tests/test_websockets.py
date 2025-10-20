"""
Tests for WebSocket event handlers.

This test suite verifies all Socket.IO events including:
- Connection/disconnection
- Message sending and receiving
- Agent status updates
- Workflow updates
- Error handling

NOTE: Flask-SocketIO test client has limitations in test mode where emitted
events don't trigger handlers properly. These tests verify the basic connection
but skip complex event testing. WebSocket functionality is verified through:
1. Manual testing with the frontend
2. Integration tests (test_integration.py)
3. Playwright E2E tests

For production, consider using real WebSocket clients for integration testing.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# Mark all WebSocket tests as integration tests
pytestmark = pytest.mark.integration


class TestWebSocketConnection:
    """Tests for WebSocket connection lifecycle."""

    def test_client_connect(self, app):
        """Test WebSocket client connection."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            assert socketio_client.is_connected()

            # Should receive connection_response event
            received = socketio_client.get_received()
            assert len(received) > 0
            assert received[0]["name"] == "connection_response"
            assert received[0]["args"][0]["status"] == "connected"

            socketio_client.disconnect()

    def test_client_disconnect(self, app):
        """Test WebSocket client disconnection."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            assert socketio_client.is_connected()

            socketio_client.disconnect()
            assert not socketio_client.is_connected()


class TestSendMessage:
    """Tests for send_message WebSocket event."""

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_send_message_success(self, mock_get_service, app):
        """Test successful message sending to agent."""
        from app import socketio

        # Mock agent service
        mock_service = MagicMock()
        mock_service.send_message_to_agent = AsyncMock(
            return_value={
                "success": True,
                "response": "Hello! I'm the test agent.",
                "agent_name": "Test Agent",
                "status": "idle",
            }
        )
        mock_get_service.return_value = mock_service

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send message
            socketio_client.emit(
                "send_message", {"agent_id": 1, "message": "Hello agent"}
            )

            # Get responses
            received = socketio_client.get_received()

            # Should receive agent_status (busy), agent_response, agent_status (idle)
            assert len(received) >= 2

            # Verify agent status
            status_events = [r for r in received if r["name"] == "agent_status"]
            assert len(status_events) >= 1

            # Verify agent response
            response_events = [r for r in received if r["name"] == "agent_response"]
            assert len(response_events) == 1
            response = response_events[0]["args"][0]
            assert response["agent_id"] == 1
            assert response["message"] == "Hello! I'm the test agent."
            assert response["sender"] == "agent"

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_send_message_missing_agent_id(self, mock_get_service, app):
        """Test sending message without agent_id."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send message without agent_id
            socketio_client.emit("send_message", {"message": "Hello"})

            # Should receive error
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            assert "agent_id and message required" in error_events[0]["args"][0]["error"]

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_send_message_missing_message(self, mock_get_service, app):
        """Test sending message without message content."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send without message
            socketio_client.emit("send_message", {"agent_id": 1})

            # Should receive error
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            assert "agent_id and message required" in error_events[0]["args"][0]["error"]

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_send_message_agent_error(self, mock_get_service, app):
        """Test message sending when agent returns error."""
        from app import socketio

        # Mock agent service to return error
        mock_service = MagicMock()
        mock_service.send_message_to_agent = AsyncMock(
            return_value={"success": False, "error": "Agent processing failed"}
        )
        mock_get_service.return_value = mock_service

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send message
            socketio_client.emit(
                "send_message", {"agent_id": 1, "message": "Hello"}
            )

            # Should receive error and status update
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            assert "Agent processing failed" in error_events[0]["args"][0]["error"]

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_send_message_not_initialized(self, mock_get_service, app):
        """Test message sending when agent system not initialized."""
        from app import socketio

        # Mock agent service to raise RuntimeError
        mock_service = MagicMock()
        mock_service.send_message_to_agent = AsyncMock(
            side_effect=RuntimeError("Agent system not initialized")
        )
        mock_get_service.return_value = mock_service

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send message
            socketio_client.emit(
                "send_message", {"agent_id": 1, "message": "Hello"}
            )

            # Should receive error with hint
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            error_data = error_events[0]["args"][0]
            assert "Agent system not initialized" in error_data["error"]
            assert "hint" in error_data


class TestAgentStatusRequest:
    """Tests for agent_status_request WebSocket event."""

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_agent_status_request_success(self, mock_get_service, app):
        """Test successful agent status request."""
        from app import socketio

        # Mock agent service
        mock_service = MagicMock()
        mock_service.get_agent_status = MagicMock(
            return_value={
                "agent_id": 1,
                "name": "Test Agent",
                "status": "idle",
                "type": "test",
            }
        )
        mock_get_service.return_value = mock_service

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Request agent status
            socketio_client.emit("agent_status_request", {"agent_id": 1})

            # Should receive agent_status event
            received = socketio_client.get_received()
            status_events = [r for r in received if r["name"] == "agent_status"]
            assert len(status_events) == 1
            status = status_events[0]["args"][0]
            assert status["agent_id"] == 1
            assert status["name"] == "Test Agent"

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_agent_status_request_missing_id(self, mock_get_service, app):
        """Test agent status request without agent_id."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Request without agent_id
            socketio_client.emit("agent_status_request", {})

            # Should receive error
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            assert "agent_id required" in error_events[0]["args"][0]["error"]


class TestWorkflowUpdate:
    """Tests for workflow_update WebSocket event."""

    def test_workflow_update_success(self, app):
        """Test successful workflow update broadcast."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send workflow update
            socketio_client.emit(
                "workflow_update",
                {
                    "workflow_id": 1,
                    "status": "running",
                    "message": "Workflow started",
                },
            )

            # Should receive workflow_status event
            received = socketio_client.get_received()
            workflow_events = [r for r in received if r["name"] == "workflow_status"]
            assert len(workflow_events) == 1
            workflow = workflow_events[0]["args"][0]
            assert workflow["workflow_id"] == 1
            assert workflow["status"] == "running"

    def test_workflow_update_missing_id(self, app):
        """Test workflow update without workflow_id."""
        from app import socketio

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send without workflow_id
            socketio_client.emit("workflow_update", {"status": "running"})

            # Should receive error
            received = socketio_client.get_received()
            error_events = [r for r in received if r["name"] == "error"]
            assert len(error_events) == 1
            assert "workflow_id required" in error_events[0]["args"][0]["error"]


class TestWebSocketIntegration:
    """Integration tests for WebSocket events."""

    @patch("app.sockets.chat_socket.get_agent_service")
    def test_multiple_messages_sequential(self, mock_get_service, app):
        """Test sending multiple messages sequentially."""
        from app import socketio

        # Mock agent service
        mock_service = MagicMock()
        mock_service.send_message_to_agent = AsyncMock(
            return_value={
                "success": True,
                "response": "Response",
                "agent_name": "Test Agent",
                "status": "idle",
            }
        )
        mock_get_service.return_value = mock_service

        with app.app_context():
            socketio_client = socketio.test_client(app, namespace=None)
            socketio_client.get_received()  # Clear

            # Send multiple messages
            for i in range(3):
                socketio_client.emit(
                    "send_message", {"agent_id": 1, "message": f"Message {i}"}
                )

            # Should receive responses for all messages
            received = socketio_client.get_received()
            responses = [r for r in received if r["name"] == "agent_response"]
            assert len(responses) == 3

    def test_connection_lifecycle(self, app):
        """Test complete connection lifecycle."""
        from app import socketio

        with app.app_context():
            # Connect
            socketio_client = socketio.test_client(app, namespace=None)
            assert socketio_client.is_connected()

            # Clear connection messages
            received = socketio_client.get_received()
            assert len(received) > 0

            # Disconnect
            socketio_client.disconnect()
            assert not socketio_client.is_connected()

            # Reconnect
            socketio_client = socketio.test_client(app, namespace=None)
            assert socketio_client.is_connected()

            # Should receive connection_response again
            received = socketio_client.get_received()
            assert any(r["name"] == "connection_response" for r in received)
