# Generating UML Diagram Images

Diagrams are organized by type in subfolders:

```
assets/
├── use-case/          (auth, secrets-authenticated, secrets-external, secrets-api, org, audit-billing)
├── class/             (user-auth, org, secret)
├── sequence/          (create-secret, generate-share, access-share)
├── activity/          (share-creation, recipient-access)
└── README-diagrams.md
```

Generate all PNGs:

```bash
cd "path/to/CIPAT"

# Use-case diagrams require mermaid-config.json for HTML actors (stick figures)
for f in use-case-auth use-case-secrets-authenticated use-case-secrets-external use-case-secrets-api use-case-org use-case-audit-billing; do
  npx --yes -p @mermaid-js/mermaid-cli mmdc -i assets/use-case/${f}.mmd -o assets/use-case/${f}.png -c mermaid-config.json
done

# Other diagrams (class, sequence, activity)
for dir in class sequence activity; do
  for f in assets/$dir/*.mmd; do
    base=$(basename "$f" .mmd)
    npx --yes -p @mermaid-js/mermaid-cli mmdc -i "$f" -o "assets/$dir/${base}.png"
  done
done
```

Or run individually, e.g.:
`mmdc -i assets/use-case/use-case-auth.mmd -o assets/use-case/use-case-auth.png -c mermaid-config.json -w 1600 -H 500`

Note: `use-case-auth.mmd` is a flat LR flowchart (no subgraph) so it renders left-to-right; use `-w 1600 -H 500` for a wide layout.
