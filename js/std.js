$(function() {
	//Set paragraph and header links to open in a new window
	//(unless they are a 'read more' link)
	$('p a, h2 a, h3 a').not('a.read_more').attr('target','_blank')
})
