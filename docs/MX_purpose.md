# Purpose of MX Data

The **MX** datasets capture experimental profit and loss calculations. They combine FDB buy (`fdbb`) and FDB sell (`fdbs`) signals with a resulting `target` column representing the outcome of each trade opportunity.

These files are derived from TTF or MLF features and live in `./data/targets/mx` or `./data/full/mx/targets` depending on the environment.

The goal is to evaluate how reliably the fractal signals translate into profit. Models can train directly on these rows to predict the `target` value.
