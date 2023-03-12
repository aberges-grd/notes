build fname:
    pandoc notes/{{fname}}.md -o build/{{fname}}.pdf -d .pandoc/defaults.yaml