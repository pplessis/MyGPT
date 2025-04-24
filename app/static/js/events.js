
/************************************  */
function createHtmlComment (Date, Texte) {
      // Création de l'élément <div class="comment">
      let comment = document.createElement('div');
      comment.className = 'comment';

      // Création des éléments <p> avec les classes "time" et "text"
      let time = document.createElement('p');
      time.className = 'time';
      time.textContent = Date; //formatDate(Date);

      let text = document.createElement('p');
      text.className = 'text';
      text.textContent = Texte;
  
      // Ajout des éléments <p> au élément <div>
      comment.appendChild(time);
      comment.appendChild(text);
  
      return comment;
  }

  function handleChatResponse(responseData, Request) {
    // Destructurer la réponse JSON
    const { status, time, message } = responseData;
    // Créer un nouvel élément de commentaire
    const commentElement = document.createElement('div');
    commentElement.className = 'comment';

    if (status === 'success') {
        commentElement.innerHTML = `
            <p class="time">${time}</p>
            <p class="name">${Request}</p>
            <hr/>
            <p class="text">${message}</p>
        `;

    } else {
        console.error('Erreur:', message);
        
        commentElement.innerHTML = `
        <p class="time"></p>
        <p class="text">🔴 Error !</p>
        `;
    }

    return commentElement
}
function formatDate(Date) {
    let dateObj = new Date(Date);
    let mois = (dateObj.getMonth() + 1).toString().padStart(2, '0');
    let jour = dateObj.getDate().toString().padStart(2, '0');
    let annee = dateObj.getFullYear();
    return `${mois}/${jour}/${annee}`;
}

function loadEvents () {
  console.log ('START load Events')

  // CONSTS
  let cadreTexte = document.getElementById('cadre-texte');
  let validBtn = document.getElementById('bouton-validated');
  let loader = document.getElementById('loader');
  let comments = document.getElementById('comments');
  let comment = ''

  validBtn.addEventListener('click', async () => {
      loader.style.display = 'block';
      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            message: cadreTexte.value.trim() // Ajouter une valeur par défaut
          })
        });
        if (response.ok) {
          const texte = cadreTexte.value;
          console.log(texte);
          const responseData = await response.json();
          console.log("Reponse /chat:", responseData);
          // Récupération du contenu de la réponse

          comment = handleChatResponse(responseData, cadreTexte.value.trim())

          console.log(comment.outerHTML);           // Affiche le contenu du commentaire créé

          // Vider le champ de texte
          document.getElementById('cadre-texte').value = '';

        } else {
          console.error('Erreur:', response.status, response.statusText);
          const responseData = await response.json();
          comment = handleChatResponse(responseData, cadreTexte.value.trim())
        }
      } catch (erreur) {
        console.error(erreur);
      } finally {
        comments.appendChild(comment)
        loader.style.display = 'none';
      }
    });

  console.log ('END load Events')
}

function loadBanner () {
  console.log ('START load banner')
silktideCookieBannerManager.updateCookieBannerConfig({
  background: {
    showBackground: true
  },
  cookieIcon: {
    position: "bottomLeft"
  },
  cookieTypes: [
    {
      id: "necessary",
      name: "Necessary",
      description: "<p>These cookies are necessary for the website to function properly and cannot be switched off. They help with things like logging in and setting your privacy preferences.</p>",
      required: true,
      onAccept: function() {
        console.log('Add logic for the required Necessary here');
      }
    },
    {
      id: "analytics",
      name: "Analytical",
      description: "<p>These cookies help us improve the site by tracking which pages are most popular and how visitors move around the site.</p>",
      defaultValue: true,
      onAccept: function() {
        gtag('consent', 'update', {
          analytics_storage: 'granted',
        });
        dataLayer.push({
          'event': 'consent_accepted_analytics',
        });
      },
      onReject: function() {
        gtag('consent', 'update', {
          analytics_storage: 'denied',
        });
      }
    },
    {
      id: "advertising",
      name: "Advertising",
      description: "<p>These cookies provide extra features and personalization to improve your experience. They may be set by us or by partners whose services we use.</p>",
      onAccept: function() {
        gtag('consent', 'update', {
          ad_storage: 'granted',
          ad_user_data: 'granted',
          ad_personalization: 'granted',
        });
        dataLayer.push({
          'event': 'consent_accepted_advertising',
        });
      },
      onReject: function() {
        gtag('consent', 'update', {
          ad_storage: 'denied',
          ad_user_data: 'denied',
          ad_personalization: 'denied',
        });
      }
    }
  ],
  text: {
    banner: {
      description: "<p>We use cookies on our site to enhance your user experience, provide personalized content, and analyze our traffic. <a href=\"https://your-website.com/cookie-policy\" target=\"_blank\">Cookie Policy.</a></p>",
      acceptAllButtonText: "Accept all",
      acceptAllButtonAccessibleLabel: "Accept all cookies",
      rejectNonEssentialButtonText: "Reject non-essential",
      rejectNonEssentialButtonAccessibleLabel: "Reject non-essential",
      preferencesButtonText: "Preferences",
      preferencesButtonAccessibleLabel: "Toggle preferences"
    },
    preferences: {
      title: "Customize your cookie preferences",
      description: "<p>We respect your right to privacy. You can choose not to allow some types of cookies. Your cookie preferences will apply across our website.</p>",
      creditLinkText: "",
      creditLinkAccessibleLabel: ""
    }
  },
  position: {
    banner: "bottomCenter"
  }
});

console.log ('END load banner')

}