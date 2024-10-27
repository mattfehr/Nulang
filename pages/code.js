async function runCode() {
    let interpreterCode = document.getElementById('interpreter-id');
    let terminalOutput = document.getElementById('terminal-id');

    const response = await fetch('/run-code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            code: interpreterCode.value
        })
    });

    const result = await response.json();
    terminalOutput.innerHTML = result.output.replace(/\n/g, "<br />");
}
