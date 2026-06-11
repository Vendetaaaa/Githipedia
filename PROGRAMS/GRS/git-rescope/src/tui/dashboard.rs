// idk

use anyhow::Result;
use crossterm::{
    event::{self, DisableMouseCapture, EnableMouseCapture, Event, KeyCode, KeyModifiers},
    execute,
    terminal::{disable_raw_mode, enable_raw_mode, EnterAlternateScreen, LeaveAlternateScreen},
};
use ratatui::{
    backend::CrosstermBackend,
    layout::{Alignment, Constraint, Direction, Layout, Rect},
    style::{Color, Modifier, Style},
    text::{Line, Span},
    widgets::{
        Block, BorderType, Borders, Cell, Paragraph, Row, Table,
        TableState, Wrap,
    },
    Frame, Terminal,
};
use std::{
    io,
    time::{Duration, Instant},
};

use crate::storage::{
    config::AppConfig,
    schema::Snapshot,
    store::load_store,
};

enum Screen {
    Snapshots,
    Detail(usize),
    Help,
}

struct App {
    snapshots: Vec<Snapshot>,
    table_state: TableState,
    screen: Screen,
    status_msg: Option<(String, Instant)>,
    filter: String,
    filter_mode: bool,
}

impl App {
    fn new(snapshots: Vec<Snapshot>) -> Self {
        let mut table_state = TableState::default();
        if !snapshots.is_empty() {
            table_state.select(Some(0));
        }
        Self {
            snapshots,
            table_state,
            screen: Screen::Snapshots,
            status_msg: None,
            filter: String::new(),
            filter_mode: false,
        }
    }

    fn filtered_snapshots(&self) -> Vec<&Snapshot> {
        if self.filter.is_empty() {
            self.snapshots.iter().collect()
        } else {
            let f = self.filter.to_lowercase();
            self.snapshots
                .iter()
                .filter(|s| {
                    s.description.to_lowercase().contains(&f)
                        || s.branch.to_lowercase().contains(&f)
                        || s.id.contains(&f)
                })
                .collect()
        }
    }

    fn selected_snapshot(&self) -> Option<&Snapshot> {
        let idx = self.table_state.selected()?;
        let filtered = self.filtered_snapshots();
        filtered.get(idx).copied()
    }

    fn next(&mut self) {
        let len = self.filtered_snapshots().len();
        if len == 0 {
            return;
        }
        let i = self.table_state.selected().map_or(0, |i| (i + 1) % len);
        self.table_state.select(Some(i));
    }

    fn previous(&mut self) {
        let len = self.filtered_snapshots().len();
        if len == 0 {
            return;
        }
        let i = self.table_state.selected().map_or(0, |i| {
            if i == 0 {
                len - 1
            } else {
                i - 1
            }
        });
        self.table_state.select(Some(i));
    }

    fn set_status(&mut self, msg: impl Into<String>) {
        self.status_msg = Some((msg.into(), Instant::now()));
    }
}

pub fn run_dashboard(config: &AppConfig) -> Result<()> {
    let store = load_store(config)?;
    let mut app = App::new(store.snapshots);

    enable_raw_mode()?;
    let mut stdout = io::stdout();
    execute!(stdout, EnterAlternateScreen, EnableMouseCapture)?;
    let backend = CrosstermBackend::new(stdout);
    let mut terminal = Terminal::new(backend)?;

    let tick_rate = Duration::from_millis(200);
    let mut last_tick = Instant::now();

    loop {
        terminal.draw(|f| draw(f, &mut app))?;

        let timeout = tick_rate
            .checked_sub(last_tick.elapsed())
            .unwrap_or(Duration::ZERO);

        if event::poll(timeout)? {
            if let Event::Key(key) = event::read()? {
                
                if app.filter_mode {
                    match key.code {
                        KeyCode::Esc => {
                            app.filter_mode = false;
                        }
                        KeyCode::Enter => {
                            app.filter_mode = false;
                        }
                        KeyCode::Backspace => {
                            app.filter.pop();
                        }
                        KeyCode::Char(c) => {
                            app.filter.push(c);
                        }
                        _ => {}
                    }
                    continue;
                }

                match key.code {
                    KeyCode::Char('q') | KeyCode::Esc => {
                        match app.screen {
                            Screen::Snapshots => break,
                            Screen::Detail(_) | Screen::Help => {
                                app.screen = Screen::Snapshots;
                            }
                        }
                    }
                    KeyCode::Char('c')
                        if key.modifiers.contains(KeyModifiers::CONTROL) =>
                    {
                        break;
                    }
                    KeyCode::Down | KeyCode::Char('j') => app.next(),
                    KeyCode::Up | KeyCode::Char('k') => app.previous(),
                    KeyCode::Enter | KeyCode::Char('d') => {
                        if let Some(snap) = app.selected_snapshot() {
                            let idx = app.table_state.selected().unwrap_or(0);
                            let _ = snap;
                            app.screen = Screen::Detail(idx);
                        }
                    }
                    KeyCode::Char('/') => {
                        app.filter_mode = true;
                    }
                    KeyCode::Char('c') => {
                        app.filter.clear();
                        app.set_status("Filter cleared");
                    }
                    KeyCode::Char('?') | KeyCode::Char('h') => {
                        app.screen = Screen::Help;
                    }
                    KeyCode::Char('r') => {
                        if let Ok(store) = load_store(config) {
                            app.snapshots = store.snapshots;
                            app.set_status("Reloaded from disk");
                        }
                    }
                    _ => {}
                }
            }
        }

        if last_tick.elapsed() >= tick_rate {
            last_tick = Instant::now();
        }
    }

    disable_raw_mode()?;
    execute!(
        terminal.backend_mut(),
        LeaveAlternateScreen,
        DisableMouseCapture
    )?;
    terminal.show_cursor()?;
    Ok(())
}

 

fn draw(f: &mut Frame, app: &mut App) {
    match &app.screen {
        Screen::Help => draw_help(f, app),
        Screen::Detail(idx) => {
            let idx = *idx;
            draw_detail(f, app, idx);
        }
        Screen::Snapshots => draw_snapshots(f, app),
    }
}

fn draw_snapshots(f: &mut Frame, app: &mut App) {
    let size = f.size();
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),
            Constraint::Min(5),
            Constraint::Length(3),
            Constraint::Length(1),
        ])
        .split(size);

    
    let header = Paragraph::new(vec![
        Line::from(vec![
            Span::styled(
                " git-rescope ",
                Style::default()
                    .fg(Color::Cyan)
                    .add_modifier(Modifier::BOLD),
            ),
            Span::styled(
                "— Development Context Manager",
                Style::default().fg(Color::Gray),
            ),
        ]),
    ])
    .block(
        Block::default()
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded)
            .style(Style::default().fg(Color::DarkGray)),
    )
    .alignment(Alignment::Left);
    f.render_widget(header, chunks[0]);

    
    let filtered = app.filtered_snapshots();
    let rows: Vec<Row> = filtered
        .iter()
        .map(|s| {
            Row::new(vec![
                Cell::from(s.short_id().to_string()).style(Style::default().fg(Color::Yellow)),
                Cell::from(s.timestamp.format("%Y-%m-%d %H:%M").to_string())
                    .style(Style::default().fg(Color::Gray)),
                Cell::from(s.branch.clone()).style(Style::default().fg(Color::Green)),
                Cell::from(s.open_files.len().to_string())
                    .style(Style::default().fg(Color::Cyan)),
                Cell::from(s.description.clone()),
            ])
        })
        .collect();

    let header_cells = ["ID", "TIMESTAMP", "BRANCH", "FILES", "DESCRIPTION"]
        .iter()
        .map(|h| Cell::from(*h).style(Style::default().fg(Color::White).add_modifier(Modifier::BOLD)));
    let header_row = Row::new(header_cells).height(1).bottom_margin(1);

    let table = Table::new(
        rows,
        [
            Constraint::Length(10),
            Constraint::Length(18),
            Constraint::Length(20),
            Constraint::Length(7),
            Constraint::Min(20),
        ],
    )
    .header(header_row)
    .block(
        Block::default()
            .borders(Borders::ALL)
            .border_type(BorderType::Rounded)
            .title(format!(" Snapshots ({}) ", filtered.len()))
            .title_style(Style::default().fg(Color::Cyan))
            .style(Style::default().fg(Color::DarkGray)),
    )
    .highlight_style(
        Style::default()
            .bg(Color::DarkGray)
            .add_modifier(Modifier::BOLD),
    )
    .highlight_symbol("▶ ");

    f.render_stateful_widget(table, chunks[1], &mut app.table_state);

    
    let (filter_text, filter_style) = if app.filter_mode {
        (
            format!(" 🔍 Filter: {}█", app.filter),
            Style::default().fg(Color::Yellow),
        )
    } else if !app.filter.is_empty() {
        (
            format!(" Filter: '{}' (press / to change, c to clear)", app.filter),
            Style::default().fg(Color::Cyan),
        )
    } else if let Some((msg, t)) = &app.status_msg {
        if t.elapsed() < Duration::from_secs(3) {
            (format!(" ✓ {msg}"), Style::default().fg(Color::Green))
        } else {
            (" Ready".to_string(), Style::default().fg(Color::DarkGray))
        }
    } else {
        (" Ready".to_string(), Style::default().fg(Color::DarkGray))
    };

    let status = Paragraph::new(filter_text)
        .style(filter_style)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .border_type(BorderType::Rounded)
                .style(Style::default().fg(Color::DarkGray)),
        );
    f.render_widget(status, chunks[2]);

    let hints = Line::from(vec![
        hint("↑↓/jk", "navigate"),
        hint("  Enter", "detail"),
        hint("  /", "filter"),
        hint("  r", "reload"),
        hint("  ?", "help"),
        hint("  q", "quit"),
    ]);
    let hints_widget = Paragraph::new(hints)
        .style(Style::default().fg(Color::DarkGray));
    f.render_widget(hints_widget, chunks[3]);
}

fn draw_detail(f: &mut Frame, app: &mut App, idx: usize) {
    let filtered = app.filtered_snapshots();
    let Some(snap) = filtered.get(idx).copied() else {
        app.screen = Screen::Snapshots;
        return;
    };

    let size = f.size();
    let chunks = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Length(3),
            Constraint::Min(10),
            Constraint::Length(1),
        ])
        .split(size);

    let header = Paragraph::new(format!(" Snapshot Detail — {}", snap.short_id()))
        .style(Style::default().fg(Color::Cyan).add_modifier(Modifier::BOLD))
        .block(
            Block::default()
                .borders(Borders::ALL)
                .border_type(BorderType::Rounded)
                .style(Style::default().fg(Color::DarkGray)),
        );
    f.render_widget(header, chunks[0]);

    let mut lines = vec![
        Line::from(vec![
            label("ID:          "),
            Span::styled(snap.id.clone(), Style::default().fg(Color::Yellow)),
        ]),
        Line::from(vec![
            label("Description: "),
            Span::raw(snap.description.clone()),
        ]),
        Line::from(vec![
            label("Branch:      "),
            Span::styled(snap.branch.clone(), Style::default().fg(Color::Green)),
        ]),
        Line::from(vec![
            label("Repository:  "),
            Span::styled(snap.repo_path.clone(), Style::default().fg(Color::Cyan)),
        ]),
        Line::from(vec![
            label("Timestamp:   "),
            Span::raw(snap.timestamp.format("%Y-%m-%d %H:%M:%S UTC").to_string()),
        ]),
        Line::from(vec![
            label("Editor:      "),
            Span::raw(snap.detected_editor.clone().unwrap_or_else(|| "none".into())),
        ]),
        Line::from(""),
        Line::from(Span::styled(
            "Open Files:",
            Style::default().fg(Color::White).add_modifier(Modifier::BOLD),
        )),
    ];

    if snap.open_files.is_empty() {
        lines.push(Line::from(Span::styled(
            "  (none)",
            Style::default().fg(Color::DarkGray),
        )));
    } else {
        for file in &snap.open_files {
            lines.push(Line::from(vec![
                Span::styled("  • ", Style::default().fg(Color::Cyan)),
                Span::raw(file.clone()),
            ]));
        }
    }

    if let Some(ref sha) = snap.patch_sha256 {
        lines.push(Line::from(""));
        lines.push(Line::from(vec![
            label("Patch SHA256: "),
            Span::styled(sha.clone(), Style::default().fg(Color::DarkGray)),
        ]));
    }

    let detail = Paragraph::new(lines)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .border_type(BorderType::Rounded)
                .title(" Details ")
                .style(Style::default().fg(Color::DarkGray)),
        )
        .wrap(Wrap { trim: false });
    f.render_widget(detail, chunks[1]);

    let hints = Line::from(vec![
        hint("q/Esc", "back"),
    ]);
    f.render_widget(Paragraph::new(hints).style(Style::default().fg(Color::DarkGray)), chunks[2]);
}

fn draw_help(f: &mut Frame, app: &mut App) {
    let size = f.size();
    let area = centered_rect(60, 80, size);

    let text = vec![
        Line::from(Span::styled(
            " git-rescope — Keyboard Shortcuts",
            Style::default().fg(Color::Cyan).add_modifier(Modifier::BOLD),
        )),
        Line::from(""),
        Line::from(Span::styled("Navigation", Style::default().add_modifier(Modifier::UNDERLINED))),
        Line::from("  ↑ / k          Previous snapshot"),
        Line::from("  ↓ / j          Next snapshot"),
        Line::from("  Enter / d      View snapshot details"),
        Line::from("  Esc / q        Go back / Quit"),
        Line::from(""),
        Line::from(Span::styled("Actions", Style::default().add_modifier(Modifier::UNDERLINED))),
        Line::from("  r              Reload snapshots from disk"),
        Line::from("  /              Enter filter mode"),
        Line::from("  c              Clear filter"),
        Line::from(""),
        Line::from(Span::styled("CLI Commands", Style::default().add_modifier(Modifier::UNDERLINED))),
        Line::from("  grs save \"msg\"   Snapshot current context"),
        Line::from("  grs list         List all snapshots"),
        Line::from("  grs restore <id> Restore a snapshot"),
        Line::from("  grs delete <id>  Delete a snapshot"),
        Line::from("  grs terms        Show Terms of Service"),
        Line::from("  grs audit-log    Show security audit log"),
        Line::from(""),
        Line::from(Span::styled(
            "  Press q or Esc to close help",
            Style::default().fg(Color::DarkGray),
        )),
    ];

    let help = Paragraph::new(text)
        .block(
            Block::default()
                .borders(Borders::ALL)
                .border_type(BorderType::Rounded)
                .title(" Help ")
                .title_style(Style::default().fg(Color::Cyan)),
        )
        .wrap(Wrap { trim: false });
    f.render_widget(ratatui::widgets::Clear, area);
    f.render_widget(help, area);
}

 

fn hint<'a>(key: &'a str, desc: &'a str) -> Span<'a> {
    Span::raw(format!("[{key}] {desc}  "))
}

fn label(s: &'static str) -> Span<'static> {
    Span::styled(s, Style::default().fg(Color::Gray))
}

fn centered_rect(percent_x: u16, percent_y: u16, r: Rect) -> Rect {
    let popup_layout = Layout::default()
        .direction(Direction::Vertical)
        .constraints([
            Constraint::Percentage((100 - percent_y) / 2),
            Constraint::Percentage(percent_y),
            Constraint::Percentage((100 - percent_y) / 2),
        ])
        .split(r);
    Layout::default()
        .direction(Direction::Horizontal)
        .constraints([
            Constraint::Percentage((100 - percent_x) / 2),
            Constraint::Percentage(percent_x),
            Constraint::Percentage((100 - percent_x) / 2),
        ])
        .split(popup_layout[1])[1]
}
