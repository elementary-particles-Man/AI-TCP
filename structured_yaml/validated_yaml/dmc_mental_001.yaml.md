# id

- path: `id`
- type: `scalar`
- required: yes

# timestamp

- path: `timestamp`
- type: `scalar`
- required: yes

# lang

- path: `lang`
- type: `scalar`
- required: yes

# phase

- path: `phase`
- type: `scalar`
- required: yes

# agent

- path: `agent`
- type: `scalar`
- required: optional

# tags

- path: `tags`
- type: `list[scalar]`
- required: optional

# meta

- path: `meta`
- type: `dict`
- required: optional

## version

- path: `meta.version`
- type: `scalar`
- required: optional

## source

- path: `meta.source`
- type: `scalar`
- required: optional

# data

- path: `data`
- type: `dict`
- required: yes

## input

- path: `data.input`
- type: `scalar`
- required: yes

## output

- path: `data.output`
- type: `scalar`
- required: yes
