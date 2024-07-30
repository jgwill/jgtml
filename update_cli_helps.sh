
clis="pncli ttfcli mlfcli jgtmlcli jgtcli jgtfxcli jgtapp"
waiter=32
tenv=jgtsd
make dev-release && echo -n "waiting a bit ($waiter) before upgrading the $tenv..." && sleep $waiter && echo "." &&  \
	(conda activate $tenv && \
		pip install -U --index-url https://test.pypi.org/simple/ jgtml && \
		echo " ">CLI_HELP.md;for cli in $clis; do echo "# $cli";echo " ";$cli --help ;echo " ";echo "----";echo " ";done>> CLI_HELP.md && \
		echo "CLI_HELP.md updated" || echo "CLI_HELP.md update failed") || echo "make dev-release failed"

