let messages = document.querySelectorAll(".message")

// Converts integer to hex 
const colToHex = (c) => {
// Hack so colors are bright enough
let color = (c < 75) ? c + 75 : c
let hex = color.toString(16);
return hex.length == 1 ? "0" + hex : hex;
}

// uses colToHex to concatenate
// a full 6 digit hex code
const rgbToHex = (r,g,b) => {
return "#" + colToHex(r) + colToHex(g) + colToHex(b);
}

// Returns three random 0-255 integers
const getRandomColor = () => {
return rgbToHex(
    Math.floor(Math.random() * 255),
    Math.floor(Math.random() * 255),
    Math.floor(Math.random() * 255));
}

// Change the font colour of each message to be a random one
for (let i = 0; i < messages.length; i++) {
    messages[i].style.color = getRandomColor();
}

// Randomize primary, secondary and tertiary colours, and set in CSS variables
let primary = getRandomColor();
let tertiary = getRandomColor();
document.documentElement.style.setProperty('--primary-col', primary);
document.documentElement.style.setProperty('--tertiary-col', tertiary);