const checklistData = [
    { title: "Check Eligibility", desc: "Ensure you meet the age and citizenship requirements to vote in your jurisdiction." },
    { title: "Register to Vote", desc: "Complete your voter registration before the deadline. You may need valid ID." },
    { title: "Find Polling Booth", desc: "Locate your designated polling station and check its opening hours." },
    { title: "Know Your Candidates", desc: "Research the candidates and propositions on your ballot to make an informed decision." },
    { title: "Understand the Ballot", desc: "Familiarize yourself with the voting machine or paper ballot layout." },
    { title: "Cast Your Vote", desc: "Bring required ID, follow instructions, and cast your vote on election day!" }
];

window.initChecklist = async function() {
    const container = document.getElementById('checklist-container');
    container.innerHTML = '';
    
    for (let i = 0; i < checklistData.length; i++) {
        const item = checklistData[i];
        
        const transTitle = await translateDynamicText(item.title, currentLanguage);
        const transDesc = await translateDynamicText(item.desc, currentLanguage);
        
        const div = document.createElement('details');
        div.className = 'checklist-item';
        div.innerHTML = `
            <summary>
                <input type="checkbox" aria-label="Mark ${transTitle} as complete"> 
                ${transTitle}
            </summary>
            <p>${transDesc}</p>
        `;
        
        container.appendChild(div);
    }
};
