<script lang="ts">
	export let projects;
</script>

<article>
	<h2>Projects</h2>
	{#each projects as project}
		<pre><code>{JSON.stringify(project)}</code></pre>
	{/each}
</article>
