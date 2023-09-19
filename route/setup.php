<?php

$whichLlmOutput = null;
$llmKeysOutput = null;

// Check if llm is available
exec('which llm 2>&1', $whichLlmOutput);

if (empty($whichLlmOutput)) {
    die("Error: llm not available. Install with 'pip install llm' or 'brew install llm'\n");
}

// Check if llm has OpenAI key set
exec('llm keys list 2>&1', $llmKeysOutput);

if (strpos(implode("\n", $llmKeysOutput), 'openai') === false) {
    echo "Get an OpenAI API key from: https://platform.openai.com/account/api-keys\n";
    passthru('llm keys set openai');
}

echo "Setup complete!\n";