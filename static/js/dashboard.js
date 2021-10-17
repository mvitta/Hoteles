
    //let toggle = document.querySelector('.container_toggle');
    //let navigation = document.querySelector('.container_navigation');
    //let main = document.querySelector('.container_main');
    //toggle.classList.toggle('active')
    //navigation.classList.toggle('active')
    //main.classList.toggle('active')

    document.querySelector('.container_toggle').addEventListener('click', function(e){
        e.preventDefault()
        let toggle = document.querySelector('.container_toggle');
        let navigation = document.querySelector('.container_navigation');
        let main = document.querySelector('.container_main');
        toggle.classList.toggle('active')
        navigation.classList.toggle('active')
        main.classList.toggle('active')
    }, false);
        





