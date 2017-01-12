#!/bin/bash

# Import utils.
source $ESDOC_WS_HOME/sh/utils.sh

# Main entry point.
main()
{
    log "update starts ..."

	cd $ESDOC_WS_HOME
	git pull
    log "shell updated"
	source $ESDOC_WS_HOME/sh/update_venv.sh
	source $ESDOC_WS_HOME/sh/custom/install.sh

    log "update complete"
}

# Invoke entry point.
main
