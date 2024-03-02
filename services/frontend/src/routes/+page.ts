const codePy = `
def decorator(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        t0 = time.monotonic()
        try:
            return func(*args, **kwargs)
        finally:
            dt = time.monotonic() - t0
            print(f"{func.__name__} took {dt:.3f} seconds")
    return decorated
`;

const codeJs = `
    const syncInterval = setInterval(async () => {
        const response = await fetch(url, {method: 'POST'});
        response.json().then((obj) => {
            console.log("Obj: " + JSON.stringify(obj));
        });
    });
`;

const codeSql = `
    WITH ranked AS (
        SELECT book_id, rank() OVER (
            PARTITION BY book_id
            ORDER BY author_id) AS some_rank
        -- will fix it later, you know
    )
    SELECT * FROM ranked JOIN some_table ON random() < 0.5;
`;

const codeSnippets = [
	{ code: codeJs, lang: 'javascript' },
	{ code: codePy, lang: 'python' },
	{ code: codeSql, lang: 'sql' }
];

async function _loadGithubRaw(url: string) {
	try {
		const resp = await fetch(url, { method: 'get' });
		if (resp.status !== 200) throw Error(`response status, expected 200, got ${resp.status}`);
		const data = await resp.json();
		return data;
	} catch (e) {
		console.warn(`Unable to download "${url}": "${e}"`);
		return [];
	}
}

async function loadProjects() {
	const projectsUrl =
		'https://raw.githubusercontent.com/tgrx/sidorov.dev/master/services/api/db/projects.json';
	return await _loadGithubRaw(projectsUrl);
}

async function loadTechStack() {
	const techstackUrl =
		'https://raw.githubusercontent.com/tgrx/sidorov.dev/master/services/api/db/techstack.json';
	return await _loadGithubRaw(techstackUrl);
}

export async function load() {
	const idx = Math.floor(Math.random() * codeSnippets.length);
	const codeSnippet = codeSnippets[idx];

	return {
		codeSnippet,
		codeSnippets,
		projects: await loadProjects(),
		techStack: await loadTechStack()
	};
}
