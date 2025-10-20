# Virtual Startup UI — Recommendations

## 1) Core problems
- **Rigid layout**: fixed-width containers, poor scaling on different screens.
- **Inconsistent UI**: mixed fonts, paddings, sizes.
- **Duplicated agent sections**: agents listed twice.
- **Text overflow**: content does not fit inside controls.
- **Awkward CLI page**: occupies full width without context.
- **Non-responsive boundaries**: top/bottom areas overflow, leaving empty space.

## 2) High‑leverage fixes
1. **Adopt responsive layout**
   - Replace fixed `px` widths with Flexbox/Grid.
   - Use `grid` with `minmax()` and `1fr`, or `flex-auto`.
   - Full-height app shell: `h-screen`, `overflow-hidden`, internal scroll areas.

2. **Unify design tokens**
   - Base font: `Inter, system-ui, sans-serif`.
   - Base size: `text-[14px]`, line-height `leading-6`.
   - Spacing scale: 4/8/12/16 px → Tailwind `1/2/3/4`.
   - Corner radius: `rounded-lg` (10–12 px).
   - Shadow: `shadow-sm` for cards, `shadow` for emphasis.

3. **Single agent list**
   - One table or list with a status indicator (dot/color).
   - Columns: *Agent*, *Role*, *Status*.
   - Sortable / filterable later; no duplication.

4. **Better information architecture**
   - **Left**: compact Agents panel.
   - **Right**: Chat as default; switchable to CLI via tabs.
   - **Bottom** (optional): resizable CLI log area for power users.

5. **Text handling**
   - Prevent overflow: `truncate`, `overflow-hidden`, `text-ellipsis`.
   - Constrain card width: `max-w-full` + internal grids.
   - Use `break-words` for long tokens if needed.

6. **Accessibility and UX**
   - Minimum touch targets `min-h-[36px]`.
   - Clear hierarchy with headings and muted labels.
   - High-contrast dark/light themes via Tailwind `dark:` variants.

## 3) Suggested layout grid
```
┌──────────────────┬─────────────────────────────────────────┐
│  Agents (left)   │  Chat (right) with tab to switch to CLI│
│  280–340 px       │  grows, scrolls; header, activity      │
├──────────────────┼─────────────────────────────────────────┤
│  (optional)      │  Bottom CLI/log pane (resizable later)  │
└──────────────────┴─────────────────────────────────────────┘
```
CSS idea:
```css
.layout {
  display: grid;
  grid-template-columns: 300px 1fr;
  grid-template-rows: 1fr auto;
  grid-template-areas:
    "sidebar main"
    "sidebar bottom";
  height: 100vh;
}
```

## 4) Implementation notes
- Use a single `DashboardLayout` shell with areas: `Sidebar`, `Main`, `Bottom`.
- Break features into React components: `AgentList`, `ChatPanel`, `CliPanel`.
- Tailwind utilities for speed; optionally add shadcn/ui later.
- Persist tab state in URL query or local storage.

