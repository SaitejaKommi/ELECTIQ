const timelineData = [
    { title: "Announcement", desc: "The Election Commission announces the schedule for the elections, bringing the Model Code of Conduct into effect." },
    { title: "Nomination", desc: "Candidates file their nomination papers, which are then scrutinized. They have a window to withdraw their nominations." },
    { title: "Campaigning", desc: "Political parties and candidates campaign to win voter support. Campaigning strictly ends 48 hours before polling." },
    { title: "Voting Day", desc: "Eligible voters cast their votes at designated polling booths using EVMs or paper ballots." },
    { title: "Counting", desc: "Votes are counted under strict security and observation on a predetermined date." },
    { title: "Certification", desc: "The Election Commission certifies the results and declares the winning candidates." },
    { title: "Inauguration", desc: "Elected officials take their oath of office and form the new government." }
];

window.initTimeline = async function() {
    const container = document.getElementById('timeline-container');
    container.innerHTML = '';
    
    for (let i = 0; i < timelineData.length; i++) {
        const item = timelineData[i];
        
        // Translate title and desc
        const transTitle = await translateDynamicText(item.title, currentLanguage);
        const transDesc = await translateDynamicText(item.desc, currentLanguage);
        
        const div = document.createElement('div');
        div.className = 'timeline-item';
        div.tabIndex = 0; // Accessible
        div.innerHTML = `<h3>${transTitle}</h3>`;
        
        div.addEventListener('click', () => showPopup(transTitle, transDesc));
        div.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') showPopup(transTitle, transDesc);
        });
        
        container.appendChild(div);
    }
};

function showPopup(title, desc) {
    const popup = document.getElementById('timeline-popup');
    document.getElementById('popup-title').textContent = title;
    document.getElementById('popup-desc').textContent = desc;
    popup.classList.remove('hidden');
}

document.getElementById('close-popup')?.addEventListener('click', () => {
    document.getElementById('timeline-popup').classList.add('hidden');
});
