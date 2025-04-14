import FingerprintJS from '{{ url_for("static", filename="scripts/fingerprintJS.js") }}';

FingerprintJS.load().then(fp => {
    fp.get().then(result => {
        const visitorId = result.visitorId;
        document.cookie = `fingerprint=${visitorId}; path=/; max-age=${60 * 60 * 24 *7}; SameSite=Lax`;
    });
});