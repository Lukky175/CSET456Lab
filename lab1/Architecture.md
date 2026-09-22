                    USER
                     │
                     │ GitHub URL
                     ▼
            ┌──────────────────┐
            │ mine_repository  │
            │      .py         │
            └────────┬─────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ repository_setup.py  │
          └──────────┬───────────┘
                     │
             clone / reuse
                     │
                     ▼
              Local Git Repo
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
 ┌─────────────────┐   ┌──────────────────────┐
 │ file_metrics.py │   │ git_history_metrics  │
 │                 │   │       .py            │
 └────────┬────────┘   └──────────┬───────────┘
          │                       │
          ▼                       ▼
 file_metrics.csv        git_history_metrics.csv
          │                       │
          └───────────┬───────────┘
                      ▼
             report_generator.py
                      │
              ┌───────┴────────┐
              ▼                ▼
      repository_        summary.md
      statistics.json