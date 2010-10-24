Prototypical foundation for a Lojban web infrastructure with a focus on Jbovlaste 2.
====================================================================================

(From the affix forms of *stuzi* as a *cmevla*, because it's not really
a *stuzi* (more like a *ciste* or a *tcana*) and because Robin loves
affix-form *cmevla*. Also, *lojbo tcana* was sort of already taken.)


So... What is this, really?
---------------------------

Not really anything - yet. I'm laying the groundwork for what hopefully will
end up being the next `jbovlaste <http://jbovlaste.lojban.org/>`_, also known
as *relvlast* and JVS2, or really any web application the community might need.
The idea is to have a solid foundation to build anything on easily.

As for Jbovlaste 2, my thinking is that it's better to start *now* building
*something* than endlessly discuss how to design it first. As we perfect the
design, it should be easy to adapt the implementation because it is built
with modern technologies and test driven development.


Great! So when can I use it?
----------------------------

Not in quite some time! Just reimplementing *jbovlaste* from scratch is a
non-trivial undertaking, and we're not even sure yet how we want to *redesign*
it. In fact, I'm working under the assumption that the Lojban server will
support Python 2.6 by the time this is deployed, something which requires
Debian to release their next stable version and Robin to update the machine.
Even *then* it might not be usable yet.


Documentation
-------------

.. toctree::
   :maxdepth: 2

   hacking
   flask
   extensions
