const {JSDOM} = require('jsdom');
const fs = require('fs');
const path = require('path');

async function crawlPage(baseUrl, currentUrl, pages, maxPages, visitedCount) {
    const baseUrlObj = new URL(baseUrl);
    const currentUrlObj = new URL(currentUrl);

    if (baseUrlObj.hostname !== currentUrlObj.hostname) {
        return { pages, visitedCount };
    }

    const normalizedCurrentUrl = normalizeURL(currentUrl);
    if (pages[normalizedCurrentUrl] > 0) {
        pages[normalizedCurrentUrl]++;
        return { pages, visitedCount };
    }

    pages[normalizedCurrentUrl] = 1;
    visitedCount++;

    console.log(`Actively crawling: ${currentUrl}`);

    if (visitedCount >= maxPages) {
        console.log(`Reached the maximum limit of ${maxPages} pages.`);
        return { pages, visitedCount };
    }

    try {
        const resp = await fetch(currentUrl);

        if (resp.status > 399) {
            console.log("Error in fetching with status code: ", resp.status, " on page: ", currentUrl);
            return { pages, visitedCount };
        }

        const contentType = resp.headers.get("content-type");
        if (!contentType.includes("text/html")) {
            console.log("Non HTML response, content type: ", contentType, " on page: ", currentUrl);
            return { pages, visitedCount };
        }

        const htmlBody = await resp.text();
        
        // writeHTML(normalizedCurrentUrl, htmlBody);

        const nextUrls = getURLsFromHTML(htmlBody, baseUrl);

        for (const nextUrl of nextUrls) {
            if (visitedCount >= maxPages) {
                break;
            }
            const result = await crawlPage(baseUrl, nextUrl, pages, maxPages, visitedCount);
            pages = result.pages;
            visitedCount = result.visitedCount;
        }
    } catch (err) {
        console.log(`Error fetching from: `, currentUrl, err.message);
    }

    return { pages, visitedCount };
}

function getURLsFromHTML(htmlBody, baseURL){
    const urls = [];
    const dom = new JSDOM(htmlBody)
    const linkElements = dom.window.document.querySelectorAll('a')
    for(linkElement of linkElements){
        if(linkElement.href.slice(0, 1) === '/'){
            // relative
            try{
                const urlObj = new URL(`${baseURL}${linkElement.href}`)
                urls.push(urlObj.href)
            }catch(err){
                console.log("error with relative URL:", err.message);
            }
        }else{
            //absolute
            try{
                const urlObj = new URL(linkElement.href)
                urls.push(urlObj.href);
            }catch(err){
                console.log("error with absolute URL:", err.message);
            }
        }
    }
    return urls;
}

// the job of normalizeURL function is to take in the input urls and then return 
// same output for the URLs that lead to the same page
// example: 'http://www.boot.dev', 'http://www.BooT.dev', 'https://www.boot.dev' -> Although these three might look different
// All these URLs obviously lead to the same page. So, we want the normalizeURL function to return same output URL 
// for all these URLs, like 'boot.dev'
function normalizeURL(urlString) {
    const urlObj = new URL(urlString);
    const hostPath = `${urlObj.hostname}${urlObj.pathname}`;
    if(hostPath.length > 0 && hostPath.slice(-1) === '/'){
        return hostPath.slice(0, -1);
    }
    return hostPath;
}

function writeHTML(urlPath, htmlBody) {
    // Sanitize the URL path to use as a file name
    const sanitizedPath = urlPath.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    const filePath = path.join(__dirname, 'arxiv_crawled_pages', `${sanitizedPath}.html`);

    fs.mkdirSync(path.dirname(filePath), { recursive: true });
    fs.writeFileSync(filePath, htmlBody);
    console.log(`Saved HTML for ${urlPath} to ${filePath}`);
}

async function saveMainUrl(urlPath) {
    // Sanitize the URL path to use as a file name
    const sanitizedPath = urlPath.replace(/[^a-z0-9]/gi, '_').toLowerCase();
    // const filePath = path.join(__dirname, 'arxiv_crawled_pages', `${sanitizedPath}.html`);
    const filePath = path.join(__dirname, 'arxiv_crawled_pages', `https://arxiv.org.html`);
    try {
        const resp = await fetch(urlPath);

        if (resp.status > 399) {
            console.log("Error in fetching with status code: ", resp.status, " on page: ", urlPath);
            return;
        }

        const contentType = resp.headers.get("content-type");
        if (!contentType.includes("text/html")) {
            console.log("Non HTML response, content type: ", contentType, " on page: ", urlPath);
            return;
        }

        const htmlBody = await resp.text();

        fs.mkdirSync(path.dirname(filePath), { recursive: true });
        fs.writeFileSync(filePath, htmlBody);
        console.log(`Saved HTML for ${urlPath} to ${filePath}`);
    } catch (err) {
        console.log(`Error fetching from: `, urlPath, err.message);
    }
}

module.exports = {
    normalizeURL,
    getURLsFromHTML,
    crawlPage,
    writeHTML,
    saveMainUrl
}