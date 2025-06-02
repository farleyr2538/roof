# ROOF

**Background**

I first got the idea for Roof when I worked as an Estate Agent (Realtor for rentals in American) in London. It was clear that those who were able
to speak to the existing tenants before making an offer on a property had a concrete advantage compared to those who weren't able to speak to the
previous tenants. It struck me that there is no transparency in the lettings business, and no form of accountability. In everything else in the
economy, you can find a rating or review beforehand to ensure the seller/provider is trusted. But when it comes to the biggest expense that people
make in a year - renting - there was no clarity whatsoever. Landlords are often unresponsive or neglectful, because there are no consequences for
poor behaviour.

Part of why I am so passionate about Roof is that it is predominantly younger, poorer people who are trying to find their feet in the city who
are the victims of bad or unscrupulous landlords, who are typically older and more wealthy. Tenants who get the worst of it are often new to the
country, don't speak much English, or are students.

Since then, I have tried to make Roof a reality. I used Squarespace for time, but found that I could not build the features that I wanted, like
connecting to a database. For a time a developer took interest and volunteered to build it, but then they went quiet on me and stopped responding.

This is why I took CS50. To build it for real. For my final project, I have built a minimum viable product which does the basics, and only the basics.

**Project Outline**

In terms of the actual website, it runs on 'app.py.' The page layout can be found in 'templates', along with all the other pages. The page allows users
to rate their landlords, either on the homescreen or on the standalone '/rate' page (for linking to when outreaching). These reviews then feed into
the 'project.db' database, with a first name, last name, address of the property in question, postcode, rating, years spent at the property, and
a timestamp of when the review was submitted. As you may see, there are a few tests my girlfriend and I did to make sure it worked!

This information is visible on the '/find-rating' page, where the contents of the 'reviews' table is printed out into a table, similar to 'Finance.'
This page allows you to either browse through the ratings, or search for a specific review by address or postcode. Once you have searched, you can
easily get back to viewing all the reviews by clicking the 'show all ratings' button. It was very satisfying being able to do this, having struggled
trying to find how to do this is Squarespace for so long! I had been worried about the difficulty of doing this, but actually Week 9 - Finance was
great preparation.

As a bonus, I made the website support dark mode. This was a fun extra, and by trawling through JavaScript documentation I found how to sense
the user's preferred visual mode and adjust for it. Initially, I was going to have a toggle, but defaulting to the user's pre-existing preference just
made much more sense and was more elegant in terms of design.
