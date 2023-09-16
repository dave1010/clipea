<?php
// basic CLI functions

function stream_exec(string $cmd, int $chunkSize = 1): Generator {
    $descriptorspec = [
        1 => ['pipe', 'w'],  // stdout
    ];

    $pipes = [];
    $process = proc_open($cmd, $descriptorspec, $pipes);

    if (is_resource($process)) {
        while (!feof($pipes[1])) {
            yield fread($pipes[1], $chunkSize);
        }
        
        // Clean up
        fclose($pipes[1]);
        proc_close($process);
    }
}

function maybe_passthru($cmd) {
    // Zsh magic
    $outputFile = getenv('COMMAND_OUTPUT_FILE');
    if ($outputFile) {
        // Let clipea.zsh handle running the command
        file_put_contents($outputFile, $cmd);
        exit;
    }


    echo "\033[0;36mExecute? [y/N] \033[0m";

    $input = strtolower(trim(fgets(STDIN)));

    if ($input !== 'y') {
        return;
    }

    passthru($cmd);
}

function get_stdin() {
    $dataFromStdin = "";
    if (!posix_isatty(STDIN)) {
        while (!feof(STDIN)) {
            $dataFromStdin .= fgets(STDIN);
        }
    }
    return $dataFromStdin;  
}