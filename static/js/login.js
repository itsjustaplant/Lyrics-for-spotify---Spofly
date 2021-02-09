const setImage = () => {
    const artwork = document.getElementById('artwork-1')
    const body = document.getElementById('body')
    const download_button = document.getElementById('download-button')
    const login_button = document.getElementById('login-button')
    const div_left = document.getElementById('div-left')
    const trademark = document.getElementById('trademark')
    const main = document.getElementById('main')
    const apple_logo = document.getElementById('apple-emoji')
    const spotify_icon = document.getElementById('spotify-icon')
    const spotify_embed = document.getElementById('track-embed')

    const artworks = [
        "https://i.scdn.co/image/ab67616d0000b2731d7dc9072977fd651a68cee7",
        "https://i.scdn.co/image/ab67616d0000b273af6e053829e96cba11f37458",
        "https://i.scdn.co/image/ab67616d0000b273b5c1c350bb0ea8aecc0cfa1b",
        "https://i.scdn.co/image/ab67616d0000b273b4ba26e47ec417f3a99f6ac4",
        "https://i.scdn.co/image/ab67616d0000b2733198dc8920850509e8a07d8c",
        "https://i.scdn.co/image/ab67616d0000b273db33259106ebbabce555b745",
        "https://i.scdn.co/image/ab67616d0000b2732b1720e2191bb963cb399b39",
        "https://i.scdn.co/image/ab67616d0000b2734600f2625644736d2f4705d8",
        "https://i.scdn.co/image/ab67616d0000b2735735e2db2b8a17f50ee15ff4",
        "https://i.scdn.co/image/ab67616d0000b2735eb35e73aecea13ce7af9264",
        "https://i.scdn.co/image/ab67616d0000b2739acf7c91ac1ff6b0bd912b15",
        "https://i.scdn.co/image/ab67616d0000b27364d3c7922de5f2e4a9c47b5e"
    ]
    const embeds = [
        "https://open.spotify.com/embed/track/3Y8JSCYjFznthCYb5HZ8lW",
        "https://open.spotify.com/embed/track/7vOpQvYKJyDz5iWVbFOOpu",
        "https://open.spotify.com/embed/track/5xHwAQiKx72cDuMCVkEF79",
        "https://open.spotify.com/embed/track/4l5nn3zlcrKSB1eyfuWHhu",
        "https://open.spotify.com/embed/track/6jcXmxtze9UHyqVePFC6dI",
        "https://open.spotify.com/embed/track/0KoN8xz4Q7kfziwK5gog4m",
        "https://open.spotify.com/embed/track/4sI9hj8M0jzbKD9vckx28J",
        "https://open.spotify.com/embed/track/40iGKElhhMK9o9lgxByXrb",
        "https://open.spotify.com/embed/track/5XR4V6uo2NCLkke1DyOcPY",
        "https://open.spotify.com/embed/track/4za14AoFYpV1BgxUKiDrJp",
        "https://open.spotify.com/embed/track/0yPwLZowcF91ZkTBsyW7Fx",
        "https://open.spotify.com/embed/track/2slzepVFBJoYTa5lTWQXGO",
    ]
    const colours = [
        ["#f9d219", "#212121"],
        ["#e7c095", "#212121"],
        ["#161616", "#FAFAFA"],
        ["#b1d8e6", "#212121"],
        ["#3b435a", "#FAFAFA"],
        ["#d18c81", "#212121"],
        ["#adadad", "#212121"],
        ["#e1e0e0", "#212121"],
        ["#6c3b0f", "#FAFAFA"],
        ["#7e8fa4", "#212121"],
        ["#f1f1f4", "#000000"],
        ["#c2b4ca", "#000000"]
    ]

    let random = Math.floor(Math.random() * 12)

    artwork.src = artworks[random]
    body.style.backgroundColor = colours[random][0]
    main.style.backgroundColor = colours[random][0]
    login_button.style.color = colours[random][0]
    download_button.style.color = colours[random][0]
    login_button.style.backgroundColor = colours[random][1]
    download_button.style.backgroundColor = colours[random][1]
    div_left.style.color = colours[random][1]
    trademark.style.color = colours[random][1]
    spotify_embed.src = embeds[random]
    if(colours[random][1] === "#FAFAFA"){
        apple_logo.style.color = "#212121"
        spotify_icon.src = "../static/images/Spotify_Icon_RGB_Black.png"
    } else{
        apple_logo.style.color = "#FAFAFA"
        spotify_icon.src = "../static/images/Spotify_Icon_RGB_White.png"
    }
}
setImage()