$(function() {
	//Set paragraph and header links to open in a new window
	//(unless they are a 'read more' link)
	$('.blanktarget').not('a.read_more').attr('target','_blank')
})
