console.log('[Y2Mate] Script lancé');

(async () => {
    // On bloque la ré-exécution, mais si erreur on reset le flag
    if (localStorage.getItem("already_ran_y2mate") === "true") {
        console.log("[Y2Mate] Script déjà exécuté → arrêt");
        localStorage.removeItem("already_ran_y2mate");
        return;
    }
    localStorage.setItem("already_ran_y2mate", "true");

    function wait(ms) { return new Promise(resolve => setTimeout(resolve, ms)); }

    try {
        // 1️⃣ Coller le lien
        const input = document.querySelector('input#v');
        if (input) {
            input.focus();
            const clip = await navigator.clipboard.readText();
            input.value = clip;
            console.log("✅ Lien collé :", clip);
        } else { throw new Error("❌ Champ de saisie non trouvé"); }

        await wait(500);

        // 2️⃣ Sélectionner MP3
        const formatBtn = document.querySelector('#f');
        if (formatBtn && formatBtn.textContent.trim().toLowerCase() !== 'mp3') {
            formatBtn.click();
            console.log("✅ Format changé en MP3");
        } else { console.log("🎵 Format déjà en MP3"); }

        await wait(500);

        // 3️⃣ Convert
        const convertBtn = [...document.querySelectorAll('button')]
            .find(btn => btn.textContent.trim().toLowerCase() === 'convert');
        if (convertBtn) { convertBtn.click(); console.log("🔄 Conversion lancée..."); }
        else { throw new Error("❌ Bouton Convert introuvable"); }

        // 4️⃣ Download
        let downloadBtn = null;
        for (let i = 0; i < 200; i++) {
            await wait(500);
            downloadBtn = [...document.querySelectorAll('button')]
                .find(btn => btn.textContent.trim().toLowerCase() === 'download');
            if (downloadBtn) break;
        }
        if (downloadBtn) { downloadBtn.click(); console.log("⬇️ Téléchargement lancé !"); }
        else { throw new Error("❌ Bouton Download introuvable"); }

        await wait(1000);

        // 5️⃣ Home
        let home = [...document.querySelectorAll('a')]
            .find(a => a.textContent.trim().toLowerCase() === "home");
        if (!home) {
            // tente de trouver le logo en fallback si le texte n'existe pas
            home = document.querySelector('a[href="/en-00uN/"]');
        }
        if (home) {
            console.log("🏠 Retour à l'accueil...");
            localStorage.setItem("already_ran_y2mate", "true");
            home.click();
        } else { throw new Error("❌ Lien Home introuvable"); }

    } catch (err) {
        console.warn("[Y2Mate]", err);
        localStorage.removeItem("already_ran_y2mate");
    }
})();
