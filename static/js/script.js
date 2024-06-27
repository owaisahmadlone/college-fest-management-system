function changeReadMore(eventId) {
    
    const myButton = document.getElementById('read-more-btn-'+eventId);
    const threeDots = document.getElementById('three-dots-'+eventId);
    const fullDesc = document.getElementById('full-desc-'+eventId);
    const eventTiming = document.getElementById('event-timings-'+eventId);

    if (fullDesc.style.display === 'none' || fullDesc.style.display === '') {
        fullDesc.style.display = 'inline';
        threeDots.style.display = 'none';
        myButton.textContent = 'Read Less';
        eventTiming.style.display = 'none';
    } 
    
    else {
        fullDesc.style.display = 'none';
        threeDots.style.display = 'inline';
        myButton.textContent = 'Read More';
        eventTiming.style.display = 'flex';
    }
}

function toggleDiv1() {
    var div = document.getElementById('profile-tab');
    var div2 = document.getElementById('organise-tab');
    var div3 = document.getElementById('edit-tab');
    var profile = document.getElementById('pf-content');
    var organise = document.getElementById('organise-content');
    var edit = document.getElementById('edit-content');
    div.style.backgroundColor = "#F2EFF3";
    div.style.color = "#4F708D"
    profile.style.display = "flex";
    div2.style.backgroundColor = "inherit";
    div2.style.color = "inherit";
    organise.style.display = "none";
    div3.style.backgroundColor = "inherit";
    div3.style.color = "inherit";
    edit.style.display = "none";
}
function toggleDiv2() {
    var div = document.getElementById('profile-tab');
    var div2 = document.getElementById('organise-tab');
    var div3 = document.getElementById('edit-tab');
    var profile = document.getElementById('pf-content');
    var organise = document.getElementById('organise-content');
    var edit = document.getElementById('edit-content');
    div2.style.backgroundColor = "#F2EFF3";
    div2.style.color = "#4F708D";
    organise.style.display = "inherit";
    div.style.backgroundColor = "inherit";
    div.style.color = "inherit";
    profile.style.display = "none";
    div3.style.backgroundColor = "inherit";
    div3.style.color = "inherit";
    edit.style.display = "none";

}
function toggleDiv3() {
    var div = document.getElementById('profile-tab');
    var div2 = document.getElementById('organise-tab');
    var div3 = document.getElementById('edit-tab');
    var profile = document.getElementById('pf-content');
    var organise = document.getElementById('organise-content');
    var edit = document.getElementById('edit-content');
    div3.style.backgroundColor = "#F2EFF3";
    div3.style.color = "#4F708D";
    edit.style.display = "inherit";
    div.style.backgroundColor = "inherit";
    div.style.color = "inherit";
    profile.style.display = "none";
    div2.style.backgroundColor = "inherit";
    div2.style.color = "inherit";
    organise.style.display = "none";
}

function toggleReadDesc(eventId) {
    var more = document.getElementById("expand-more-"+eventId);
    var less = document.getElementById("expand-less-"+eventId);
    var desc = document.getElementById("event-desc-"+eventId);
    var details = document.getElementById("event-handling-"+eventId);

    if (desc.style.display === 'none' || desc.style.display === '') {
        desc.style.display = 'inline';
        more.style.display = 'none';
        less.style.display = 'inline';
        details.style.display = 'flex';
    }
    else {
        desc.style.display = 'none';
        more.style.display = 'inline';
        less.style.display = 'none';
        details.style.display = 'none';
    }
}

function loadState(state) {
    switch(state) {
        case 0:
            toggleDiv1();
            break;
        case 1:
            toggleDiv2();
            break;
    }
}