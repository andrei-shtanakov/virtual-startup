export type TerminalLineType = "command" | "output" | "error" | "success" | "info" | "system";

export interface TerminalLine {
  id: number;
  type: TerminalLineType;
  content: string;
  timestamp: Date;
}

export interface Command {
  name: string;
  description: string;
  usage: string;
  aliases?: string[];
}



