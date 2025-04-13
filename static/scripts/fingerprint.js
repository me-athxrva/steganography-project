import FingerprintJS from 'https://openfpcdn.io/fingerprintjs/v3';

FingerprintJS.load().then(fp => {
    fp.get().then(result => {
        const visitorId = result.visitorId;
        document.cookie = `fingerprint=${visitorId}; path=/; max-age=${60 * 60 * 24 *7}; SameSite=Lax`;
    });
});