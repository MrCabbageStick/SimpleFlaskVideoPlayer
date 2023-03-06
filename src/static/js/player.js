/**
 * @type {HTMLVideoElement}
 */
const video = document.querySelector("[js-player-video]");
const player = document.querySelector("[js-player]");
const controls = {
    toggle: document.querySelector("[js-player-toggle]")
};
const timestamp = document.querySelector("[js-player-timestamp]");

///// Timeline /////
const timeline = new HorizontalSlider(
    document.querySelector("[js-player-timeline]"),
    onSliderUse,
    null,
    onSliderUse,
    onSliderSetValue
);

function onSliderUse(e){
    this.elem.style.setProperty("--progress", `${this.value}%`);
    video.currentTime = video.duration * this.value / 100;
}
function onSliderSetValue(value){
    this.elem.style.setProperty("--progress", `${this.value * 100}%`);
}

///// Player controlls /////
function toggleVideo(){
    if(video.paused){
        video.play();
    }
    else{
        video.pause();
    }
}

controls.toggle.addEventListener("click", (e) => {
    toggleVideo();
});

video.addEventListener("click", e => {
    // e.preventDefault();
    toggleVideo();
});

document.addEventListener("keydown", e => {

    console.log(e.key);

    switch(e.key){

        case " ":
            e.preventDefault();
            toggleVideo();
            break;
        
        case "ArrowLeft":
            e.preventDefault(); 
            video.currentTime = video.currentTime - 10;
            break;
        
        case "ArrowRight":
            e.preventDefault(); 
            video.currentTime = video.currentTime + 10;
            break;

    }
});

function formatSeconds(seconds){
    let hours = Math.floor(seconds / 3600);
    let minutes = Math.floor((seconds - hours * 3600) / 60);
    seconds = Math.floor(seconds - hours * 3600 - minutes * 60);

    hours = hours < 10 ? "0" + hours : hours;
    minutes = minutes < 10 ? "0" + minutes : minutes;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    return `${hours}:${minutes}:${seconds}`;
}

let updateTimelineTimeout = null;
function updateTimeline(timeout){
    if(!video.paused){
        timeline.setValue( video.currentTime / video.duration );
        timestamp.innerHTML = `${formatSeconds(video.currentTime)} / ${formatSeconds(video.duration)}`;
    }
    updateTimelineTimeout = setTimeout(updateTimeline, timeout, timeout);
}

updateTimeline(10);
