async function runCode() {
    let interpreterCode = document.getElementById('interpreter-id');
    let terminalOutput = document.getElementById('terminal-id');

    try {
        const response = await fetch('/run-code', {  // Replace with your endpoint
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: interpreterCode.value  // Assuming interpreterCode is a textarea/input
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const result = await response.json();
        terminalOutput.innerHTML = result.output.replace(/\n/g, "<br />");
        /* terminalOutput.style.height = 'max-content'; */
    } catch (error) {
        console.error('Error:', error);
        terminalOutput.textContent = 'Error executing code: ' + error.message;
    }
}
