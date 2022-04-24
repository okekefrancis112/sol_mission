
document.onscroll = () => {
    if(scrollY > 100){
        document.querySelector(".navi").classList.add('active')
    }else{
        document.querySelector(".navi").classList.remove('active')
    }
}

const awe = document.querySelector(".bar")
awe.addEventListener('click', () => {
    const navListCont = document.querySelector('.nav-list-cont')
    navListCont.classList.toggle('nav-disp')
})


const modal = document.querySelector('.modal')
const readMore = document.querySelectorAll('.read')
const totalReadmore = readMore.length
const modalHeader = document.querySelector('.text-content h3')
const newsHead = document.querySelectorAll('.news-head')
const modalImage = document.querySelector('.image-placeholder img')
const modalText  = document.querySelector('.text-content p')
const populateImageContainerImage = document.querySelectorAll('.card-image')
const textContainerArray = []

for(let i = 0; i<readMore.length; i++){
    const link = readMore[i].previousElementSibling
    textContainerArray.push(link.textContent)
    
}

const blogPopulatedText = document.querySelectorAll('.paragraph')

for(let i = 0; i < blogPopulatedText.length; i++){

    const populatedTextHolder = blogPopulatedText[i].innerHTML
    blogPopulatedText[i].innerHTML = populatedTextHolder.substring(0, 200) + "..."

}

for(let i = 0; i < readMore.length; i++){
    readMore[i].addEventListener('click', ()=>{
        modalHeader.textContent = newsHead[i].textContent
        modalText.textContent = textContainerArray[i]
        modalImage.src = populateImageContainerImage[i].src
        modal.style.left = 0
    })
}