<?php
// basic LLM functions

function get_llm_response($system, $prompt, $llmOpts): Generator {
    $cmd = "llm $llmOpts -s " . escapeshellarg($system) . " " . escapeshellarg($prompt) . " 2>&1";
    yield from stream_exec($cmd, 1);
    yield PHP_EOL;
}
