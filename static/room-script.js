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
    
    // Randomize primary, secondary and tertiary colours, and set in CSS variables
    let primary = getRandomColor();
    let tertiary = getRandomColor();
    document.documentElement.style.setProperty('--primary-col', primary);
    document.documentElement.style.setProperty('--tertiary-col', tertiary);
    
    var socketio = io();
    
    const content_messages = document.querySelector(".messages");
    
    const CreateMessage = (name, message) => {
        let messageElement = document.createElement("div");
        messageElement.className = "message";
        messageElement.innerHTML = `
            <div class="from">${name}</div>
            <div class="msg">${message}</div>
        `;
        // Apply random color style directly to the new message
        messageElement.style.color = getRandomColor();
        content_messages.appendChild(messageElement); // Append the new element to the DOM
    }
    
    const CreateAnnouncement = (name, message) => {
        let announcementElement = document.createElement("div"); // Corrected variable name
        announcementElement.className = "announcement";
        announcementElement.innerHTML = `
            <div class="from">${name}</div>
            <div class="msg">${message}</div>
        `;
        // Apply random background color to the announcement
        announcementElement.style.backgroundColor = getRandomColor();
        content_messages.appendChild(announcementElement); // Append the new element to the DOM
    
        announcementElement.classList.add('fade-out');
    }
    
    socketio.on("message", (data) => {
        if (data.tag=="announcement") {
            console.log(1);
            CreateAnnouncement(data.name, data.message);
            return;
        }
        CreateMessage(data.name, data.message);
    });
    
    const SendMessage = () => {
        const msg = document.getElementById("msg-to-send");
        if (msg.value=="") {
            return;
        };
        socketio.emit("message", {data: msg.value});
        msg.value = "";
    };