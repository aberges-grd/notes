# builds pdf given a filename (e.g. `build dvc_cml` for `notes/dvc_cml.md`)
build fname:
    pandoc notes/{{fname}}.md -o build/{{fname}}.pdf -d .pandoc/defaults.yaml

# downloads APA7 citation style
get-apa:
    curl https://raw.githubusercontent.com/citation-style-language/styles/master/apa.csl > .pandoc/apa.csl