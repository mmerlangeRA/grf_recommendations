
const url = new URL(window.location.href);
const prefixUrl = "https://3fbf-2a01-cb05-9121-e400-edbe-f9cc-3d6d-ac76.ngrok-free.app/recommendations/"
const visitorId= url.searchParams.get('q');

const style = "top:40px;right:5px;position:fixed;background-color:white;box-shadow: 2px 2px 2px gray;border-radius: 3px;padding: 2px;border: 1px solid gray;"

if (visitorId) {
    getRecommendations(visitorId)
        .then(recos => {
            addRecoDiv(recos)
        })
}

async function getRecommendations(visitorId) {
    try {
        const reco_url = prefixUrl + visitorId
        const reponse = await fetch(reco_url);
        const recommendations = await reponse.json();
        reco_array = JSON.parse(recommendations)
        return reco_array
    }catch(e) {
        console.error(e)
    }
}

async function addRecoDiv(recos) {
    if (!recos || recos.length == 0) {
        return
    }
    const div = document.createElement("div")
    const title = document.createElement("p")
    title.setAttribute("style", "font-size:15px;font-weight:bold;cursor:pointer;")
    title.innerHTML = "Recommandations"
    div.appendChild(title)
    const recoDiv = document.createElement("div")
    recoDiv.setAttribute("style", "")
    div.appendChild(recoDiv)
    div.setAttribute("style", style)

    const ul = document.createElement("ul")
    //ul.setAttribute("style", "list-style:none;padding:0px;margin:0px;font-size:10px;animation-duration:0.5s;")//    display: flex;flex - direction: column;
    recoDiv.setAttribute("style", "max-height: 0;transition: max-height 0.5s ease-out;overflow:hidden;")
    recoDiv.appendChild(ul)
    recos.forEach(reco => {
        const li = document.createElement("li")
        const a = document.createElement("a")
        a.href = reco
        a.target = "_blank"
        a.innerHTML = "Lien"
        li.appendChild(a)
        ul.appendChild(li)
    })
    div.opened=false

    title.addEventListener("click", () => {
        if (!div.opened) {
            recoDiv.style.maxHeight=""
        } else {
            recoDiv.style.maxHeight = "0"
        }
        div.opened = !div.opened
    })
    document.body.appendChild(div)
}
