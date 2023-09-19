<?php

$clipeaDir = CLIPEA_DIR;
if (strpos(__DIR__, 'Cellar/clipea/') !== false) {
    // Likely a Homebrew installation
    $brewPrefix = trim(shell_exec('brew --prefix'));
    $clipeaDir = $brewPrefix . "/opt/clipea'";
}

switch($env['shell']) {
    case '-zsh':
        $cmd = "alias '??'='source " . $clipeaDir . "/clipea.zsh'";
        break;
    default:
        $cmd = "alias '??'='source " . $clipeaDir . "/clipea'";
}

// TODO: use @exec plugin to bypass llm
$prompt = "Append this line to my " . $env['shell'] . " startup file, watching out for quotes and escaping, then explain how to manually source it: " . $cmd;

