
const[edMissions, missionsTc, edSub, mtcSub, categories] = [document.querySelector('.ed-missions'),
document.querySelector('.mission-tc'),
document.querySelector('.edm-sub'),
document.querySelector('.sub'),
document.querySelector('.categories')]

categories.addEventListener('click', (event)=>{
    const identify = event.target

    if(identify.className == "ed-missions"){
                mtcSub.classList.remove('reveal')
                edSub.classList.toggle('show')
    }

    if(identify.className == "mission-tc"){
                edSub.classList.remove('show')
                mtcSub.classList.toggle('reveal')
    }
})

