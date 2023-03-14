(function() {
    'use strict';
    
    // Color palette
    besogo.RED  = '#be0119'; // Darker red (marked variant)
    besogo.LRED = '#ff474c'; // Lighter red (auto-marked variant)
    besogo.BLUE = '#0165fc'; // Bright blue (last move)
    besogo.PURP = '#9a0eea'; // Red + blue (variant + last move)
    besogo.GREY = '#929591'; // Between white and black
    besogo.GOLD = '#dbb40c'; // Tool selection
    besogo.TURQ = '#06c2ac'; // Turqoise (nav selection)
    
    besogo.BLACK_STONES = 4; // Number of black stone images
    besogo.WHITE_STONES = 11; // Number of white stone images
    
    // Makes an SVG element with given name and attributes
    besogo.svgEl = function(name, attributes) {
        var attr, // Scratch iteration variable
            element = document.createElementNS("http://www.w3.org/2000/svg", name);
    
        for ( attr in (attributes || {}) ) { // Add attributes if supplied
            if (attributes.hasOwnProperty(attr)) {
                element.setAttribute(attr, attributes[attr]);
            }
        }
        return element;
    };
    
    // Makes a stone element
    besogo.svgStone = function(x, y, color) {
        var className = "besogo-svg-greyStone"; // Grey stone by default
        if (color === -1) { // Black stone
            className = "besogo-svg-blackStone";
        } else if (color === 1) { // White stone
            className = "besogo-svg-whiteStone";
        }

        // console.log("placed at :- " + x + "//" + y + "//" + color);
    
        return besogo.svgEl("circle", {
            cx: x,
            cy: y,
            r: 42,
            'class': className
        });
    };
    
    // Makes an "X" cross at (x, y)
    besogo.svgCross = function(x, y, color) {
        var path = "m" + (x - 24) + "," + (y - 24) + "l48,48m0,-48l-48,48";
    
        return besogo.svgEl("path", {
            d: path,
            stroke: color,
            "stroke-width": 8,
            fill: "none"
        });
    };
    
    // Makes a label at (x, y)
    besogo.svgLabel = function(x, y, color, label) {
        var element,
            size;
    
        // Trims label to 3 characters
        if (label.length > 3) {
            label = label.slice(0, 2) + '…';
        }
    
        // Set font size according to label length
        switch(label.length) {
            case 1:
                size = 72;
                break;
            case 2:
                size = 56;
                break;
            case 3:
                size = 36;
                break;
        }
    
        element = besogo.svgEl("text", {
            x: x,
            y: y,
            dy: ".65ex", // Seems to work for vertically centering these fonts
            "font-size": size,
            "text-anchor": "middle", // Horizontal centering
            "font-family": "Helvetica, Arial, sans-serif",
            fill: color
        });
        element.appendChild( document.createTextNode(label) );
    
        return element;
    };
    
    })(); // END closure 