mod commands;
mod engine;
mod security;
mod storage;
mod tui;

use anyhow::Result;
use clap::{Parser, Subcommand};
use tracing::info;

use commands::{list::cmd_list, restore::cmd_restore, save::cmd_save};
use security::audit::AuditLog;
use storage::config::AppConfig;
use tui::dashboard::run_dashboard;

#[derive(Parser)]
#[command(
    name = "grs",
    version,
    about = "Snapshot & restore your complete development context",
    long_about = include_str!("../TERMS.md"),
    propagate_version = true
)]
struct Cli {
    #[arg(short, long, global = true)]
    quiet: bool,

    #[arg(short, long, global = true)]
    verbose: bool,

    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Subcommand)]
enum Commands {
    Save {
        description: String,
        #[arg(short, long)]
        yes: bool,
    },

    List {
        #[arg(short, long)]
        all: bool,
    },

    Restore {
        snapshot: String,
        #[arg(long, hide = true)]
        force: bool,
    },

    Delete {
        snapshot: String,
    },

    Ui,
    Terms,
    AuditLog {
        #[arg(short, long, default_value = "20")]
        lines: usize,
    },
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    let log_level = if cli.verbose { "debug" } else { "warn" };
    let config = AppConfig::load_or_create()?;
    let log_dir = config.data_dir().join("logs");
    std::fs::create_dir_all(&log_dir)?;
    let file_appender = tracing_appender::rolling::daily(&log_dir, "grs.log");
    let (non_blocking, _guard) = tracing_appender::non_blocking(file_appender);
    tracing_subscriber::fmt()
        .with_env_filter(tracing_subscriber::EnvFilter::new(log_level))
        .with_writer(non_blocking)
        .init();

    info!("git-rescope started");

    let audit = AuditLog::new(&config)?;
    let cmd_str = std::env::args().collect::<Vec<_>>().join(" ");
    audit.record(&cmd_str)?;

    match cli.command {
        Some(Commands::Save { description, yes }) => {
            cmd_save(&config, &description, yes, cli.quiet)?;
        }
        Some(Commands::List { all }) => {
            cmd_list(&config, all)?;
        }
        Some(Commands::Restore { snapshot, force }) => {
            cmd_restore(&config, &snapshot, force, cli.quiet)?;
        }
        Some(Commands::Delete { snapshot }) => {
            commands::delete::cmd_delete(&config, &snapshot, cli.quiet)?;
        }
        Some(Commands::Ui) | None => {
            run_dashboard(&config)?;
        }
        Some(Commands::Terms) => {
            println!("{}", include_str!("../TERMS.md"));
        }
        Some(Commands::AuditLog { lines }) => {
            audit.print_recent(lines)?;
        }
    }

    Ok(())
}
