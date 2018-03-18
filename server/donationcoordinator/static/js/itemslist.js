
$(document).ready(function() //when document loads
{

print = console.log;

function toggleClass(p, c)
{
    if(p.hasClass(c))
    {
        p.removeClass(c);
    }
    else
    {
        p.addClass(c);
    }
}

function toggleView(p)
{
    toggleClass(p, 'hidden')
}

function applyCollapse(elt)
{
    //TODO actually do this
}

var root = $('section#items form ul');

print("root elt:")
print(root)

applyCollapse(root)
});