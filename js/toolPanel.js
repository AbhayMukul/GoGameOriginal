besogo.makeToolPanel = function(container, editor) {
    'use strict';
    var element, // Scratch for building SVG images
        svg, // Scratch for building SVG images
        labelText, // Text area for next label input
        selectors = {}; // Holds selection rects

    labelText = document.createElement("input"); // Label entry text field
    labelText.type = "text";
    labelText.title = 'Next label';
    labelText.onblur = function() {
        editor.setLabel(labelText.value);
    };

    makeButtonText('Pass', 'Pass move', function(){
        var tool = editor.getTool();
        if (tool !== 'navOnly' && tool !== 'auto' && tool !== 'playB' && tool !== 'playW') {
            editor.setTool('auto'); // Ensures that a move tool is selected
        }
        editor.click(0, 0, false); // Clicking off the board signals a pass
    });

    editor.addListener(toolStateUpdate); // Set up listener for tool state updates
    toolStateUpdate({ label: editor.getLabel(), tool: editor.getTool() }); // Initialize

    // Creates text button
    function makeButtonText(text, tip, callback) {
        var button = document.createElement('input');
        button.type = 'button';
        button.value = text;
        button.title = tip;
        button.onclick = callback;
        container.appendChild(button);
    }

    // Callback for updating tool state and label
    function toolStateUpdate(msg) {
        var tool;
        if (msg.label) {
            labelText.value = msg.label;
        }
        if (msg.tool) {
            for (tool in selectors) { // Update which tool is selected
                if (selectors.hasOwnProperty(tool)) {
                    if (msg.tool === tool) {
                        selectors[tool].setAttribute('visibility', 'visible');
                    } else {
                        selectors[tool].setAttribute('visibility', 'hidden');
                    }
                }
            }
        }
    }
}; 