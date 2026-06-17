// ==============================
// CityMate JavaScript
// ==============================

// Auto close flash messages

setTimeout(() => {

    let alerts = document.querySelectorAll(".alert");

    alerts.forEach(alert => {

        let bsAlert = new bootstrap.Alert(alert);

        bsAlert.close();

    });

}, 5000);


// ==============================
// Smooth Scroll
// ==============================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {

    anchor.addEventListener('click', function(e) {

        e.preventDefault();

        document.querySelector(
            this.getAttribute('href')
        ).scrollIntoView({

            behavior: 'smooth'

        });

    });

});


// ==============================
// Card Hover Animation
// ==============================

const cards = document.querySelectorAll(
    '.service-card, .announcement-card'
);

cards.forEach(card => {

    card.addEventListener('mouseenter', () => {

        card.style.transform =
            "translateY(-10px)";

    });

    card.addEventListener('mouseleave', () => {

        card.style.transform =
            "translateY(0px)";

    });

});


// ==============================
// Complaint Search
// ==============================

const searchInput =
    document.getElementById("searchInput");

if(searchInput){

    searchInput.addEventListener("keyup", function(){

        let filter =
            this.value.toLowerCase();

        let rows =
            document.querySelectorAll(
                "#complaintTable tbody tr"
            );

        rows.forEach(row => {

            let text =
                row.textContent.toLowerCase();

            row.style.display =
                text.includes(filter)
                ? ""
                : "none";

        });

    });

}


// ==============================
// Counter Animation
// ==============================

function animateCounter(id, target){

    let element =
        document.getElementById(id);

    if(!element) return;

    let count = 0;

    let speed = target / 100;

    let interval = setInterval(() => {

        count += speed;

        if(count >= target){

            count = target;

            clearInterval(interval);

        }

        element.innerText =
            Math.floor(count);

    }, 20);

}


// Example Counter IDs

animateCounter("usersCount", 10000);
animateCounter("complaintsCount", 500);
animateCounter("servicesCount", 100);
animateCounter("updatesCount", 50);


// ==============================
// Confirm Status Update
// ==============================

const updateForms =
    document.querySelectorAll(
        '.status-update-form'
    );

updateForms.forEach(form => {

    form.addEventListener('submit', function(e){

        const confirmUpdate =
            confirm(
                "Are you sure you want to update complaint status?"
            );

        if(!confirmUpdate){

            e.preventDefault();

        }

    });

});


// ==============================
// Back To Top Button
// ==============================

const topButton =
    document.createElement("button");

topButton.innerHTML =
    '<i class="fas fa-arrow-up"></i>';

topButton.id = "topBtn";

document.body.appendChild(topButton);

topButton.style.cssText = `
position:fixed;
bottom:20px;
right:20px;
width:50px;
height:50px;
border:none;
border-radius:50%;
background:#2563eb;
color:white;
font-size:20px;
cursor:pointer;
display:none;
z-index:999;
box-shadow:0 4px 15px rgba(0,0,0,0.2);
`;

window.addEventListener("scroll", () => {

    if(window.scrollY > 300){

        topButton.style.display = "block";

    } else {

        topButton.style.display = "none";

    }

});

topButton.addEventListener("click", () => {

    window.scrollTo({

        top:0,
        behavior:"smooth"

    });

});


// ==============================
// Welcome Message
// ==============================

window.addEventListener("load", () => {

    console.log(
        "Welcome to CityMate Smart City Platform 🚀"
    );

});