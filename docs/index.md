# Physical Model Hybrids

MUMT 618 taught by Prof. Gary Scavone

Final Project by Travis West

*Abstract:*

I present a partial reimplementation of [Perry Cook's 1992 meta-wind physical
model, the Whirlwind][whirlwind], a full reimplementation of [the Blotar,
described by Stiefel et. al. in 2004][blotar], and a novel implementation of a
hybrid blown/bowed string model dubbed the Saxobowy, all using [the SOUL
programming language][soul].  In the course of this presentation, I consider my
goals in studying these models, particularly the desire to create new and
unusual sounds using physical modelling synthesis strategies.  In pursuit of
such sounds, I also consider the excitation mechanisms of the cane reed model
from a purely mathematical perspective.  I devise several alternative
clarinet-like models from these considerations.

*Playing the models:*

All of the models in the repository are SOUL patches.  The simplest way to play
with them is to install the [soul command line tool][soul command line] and
use it to invoke the patch:

```bash
cd path_to_repo
soul play name_of_patch
```

***WARNING***

Some of the models contained in this repository are un-tested experimental
hybrids, and may be unstable in certain configurations. Take precautions to
ensure that your ears and listening equipment cannot be damaged in case a model
should become unstable.

# Introduction

The design of most physical modelling synthesizers aims to produce sounds that
are authentic to a specific acoustic instrument:  an electric guitar model for
synthesizing the sound of an electric guitar, a flute model for producing the
sound of a flute, and so on.  These may be considered as authentic synthesis
models.  Although less common, it is just as musically valid to develop
physically inspired synthesis models that do not correspond to any real
acoustic object.  One way of developing such models is to combine the authentic
models of unrelated instruments into novel hybrid models.  

Two such hybrid models are [the Whirlwind][whirlwind], and [the
Blotar][blotar].  The Whirlwind synthesizer combines brass, air reed, and cane
reed models into a single meta-model capable (in principle) of modelling any of
these three instrument classes, or some combination of the three.  The Blotar
(and its relative the uBlotar) stem from the structural equivalence of simple
flute and electric guitar models, resulting in an effective hybrid model that
easily spans a wide range of characters and sonic qualities.  Another possible
hybrid is suggested by the structural similarity of [the STK's][stk] [Saxofony
model][saxofony] and [bowed string model][bowed].

No particular justification is given in the papers describing the Whirlwind and
the Blotar as to why one might want to make such hybrids in the first place.
There are some obvious features of these models that may make them attractive:

 - A hybrid model may (in principle) produce sounds characteristic of its
   constituent authentically-modelled parts.
 - A hybrid may be able to produce sounds that morph between the authentic
   parts or possess characteristics of multiple authentic parts simultaneously;
   hybrid sounds, in short.
 - A hybrid model may also be able to produce entirely novel sounds not
   possible to evoke with any of the original authentic models.

## Motivation

In my view, the desire to generate new and unusual sounds is of particular
relevance.  I recognize that there are numerous benefits to using a physical
model rather than a real acoustic instrument, there is certainly redundancy in
developing a synthesis model to produce sounds that could just as easily be
made e.g. by rubbing horse hair against a string or blowing raspberries into a
metal pipe.  Acoustic instruments already sound great and feel great to play.
Where the computer is involved, I am more captivated by the possibility to make
sounds that can't be made by other means.  Physical model hybrids offer an
interesting means of approaching this goal.

Another personal advantage gained by the study of hybrid models is that it
requires as prerequisite the study of the constituent authentic models.  In the
course of reimplementing the Whirlwind alone, three other physical models must
also be closely examined.  I enjoyed the opportunity to reimplement these
models as well, gaining a much deeper appreciation for the subtleties involved
in physical modelling synthesis using waveguides in general.

As such, the motivation for this project was threefold: reimplement a variety
of physical modelling synthesis algorithms, combine these implementations to
recreate the Whirlwind and Blotar models, and ultimately use these algorithms
to produce unique sounds that are not otherwise readily available.

## The Plan

The Whirlwind is a combination of three authentic models: a brass instrument, a
flute, and a clarinet.  The Blotar is a combination of a flute and an electric
guitar.  A novel hybrid, which I dubbed the Saxobowy, seemed possibly by
combining the STK's [Saxofony][saxofony] and [Bowed][bowed] models.  In order
to validate my work at regular intervals, I planned to reimplement the original
models and combine them to make hybrids as soon as possible.  I anticipated
that it would be difficult to make sound with the Whirlwind and Saxobowy
models, so the Blotar was implemented first.

For all of the implementations I chose [SOUL][soul] as programming language.
SOUL (the SOUnd Language) was [introduced by Julian Storer at the Audio
Developers Conference in 2018][soul announcement].  It aims to ["modernise and
optimise the way high-performance, low-latency audio code is written and
executed."][soul].  It is a domain specific language for writing audio code.
Programs are largely composed of processors, which implement DSP blocks with
certain inputs and outputs such as a delay or a filter, and graphs, which
combine processors.  It is a new language, and it has its quirks, but I am
enthusiastic about its ultimate goals and find the language expressive and fun
to write.  [The accompanying command-line tool][soul command line]
automatically generates a GUI using [JUCE][juce], which is invaluable for
testing.

# Implementing The Hybrid Models

## The Blotar

The Blotar is based on the observation that the electric guitar and the flute
can be modelled with nearly the same exact structure, illustrated in the
adjacent figure.  The two models differ only in the way they are excited, the
kind of filter used to model propagation losses, and in the interpretation of
the structure.  An electric guitar is excited by strumming on the strings,
usually implemented as inputting a burst of noise into the string delay line.
A flute is excited by blowing into the instrument, implemented as a DC offset
added to the feedback from the bore.  The plucked string of the electric guitar
may typically use a one-zero lowpass filter to model propagation losses,
whereas the losses in the bore of a flute are better modelled with a one-pole
lowpass filter. The Blotar results from combining the flute and guitar
excitation methods and allowing the loss filter to crossfade between the
one-zero and one-pole filters.

![Block diagram of the Blotar.](blotar.svg)
*Block diagram of the Blotar, annotated with the dual interpretation of its elements.*

Implementing the flute, electric guitar, and Blotar was reasonably
straightforward.  The flute model and the Blotar can be found in the
repository; the electric guitar implementation is omitted due to its similarity
and simplicity.

## The Whirlwind

The Whirlwind is based on brass, flute, and clarinet models.  The flute was
already implemented for the Blotar.  For the clarinet, [Cook][whirlwind] uses a
general third order polynomial to model the non-linearity in the reed
excitation, but provides no guidance on what coefficients may be used to
successfully produce sound.  As such, my implementation follows the STK
clarinet model since it provides unambiguous implementation details.

Having implemented the flute and clarinet, I turned to the issue of combining
the two.  Here again, Cook does not provide any advice on how to go about the
combination.  A few different approaches occurred to me, however.

Consider the equation for the reed model as employed in the STK, with inputs of breath pressure (`h`) and the reflection from the bore (`r`):

```
x = -0.95 * r - h
y = x * (-m * x + b) + h
```

Where `m` is the slope of the reed table, related to reed stiffness, and `b` is
the offset of the reed table, associated with initial reed opening size, and
where clipping is neglected for the simplicity of the presentation (the model
still produces sound even without clipping).

The flute has a non-linearity of the form

```
x = -0.45 * r - h
y = x * x * x - x
```

which could be rewritten:

```
y = x * (x * x - 1)
```

Given the latter formulation, I initially tried to combine the two models by
using an excitation of the following form:

```
x = -g * r - h
y = x * (-s * m * x + (1 - s) * x * x + b) + q * h
```

where `s`, `q`, and `b` could be varied to alternate between the two models.
This approach was unsuccessful; although the flute or the clarinet sounds could
be reproduced, nothing interesting could be found in between.

A more successful approach was found to be the following form:

```
xc = -0.95 * r - h
xf = -0.45 * r + h
c = xc * ( m * xc + b) + h
f = xf * (xf * xf - 1)
y = F * f + C * c
```

where `F` and `C` are used to mix the two models to varying degrees.  Using
this combination, I found I was able to produce sound with a bit of clarinet
non-linearity and a bit of flute non-linearity.  The model was still not
particularly responsive or satisfying, particularly when trying to morph
between the two excitation models, but it was at least somewhat operational.

More success and satisfaction was found from the combination of the delay-line
structures of the flute and clarinet, incorporating both a jet-delay and a
second delay parallel to the bore for modelling tone-hole effects.  These delay
lines provided immediate and satisfying behaviors combining characteristics of
both original models.


I was ultimately unable to successfully implement the brass model, for reasons
that remain unclear to me, and despite very carefully studying the
implementation in the STK as an example.  In the interest of time, I ultimately
abandoned the brass model entirely, focusing instead on the Saxobowy.  The
flute and clarinet implementations are available in the repository, as is the
"clarinute" model that combines the two.

![Block diagram of the clarinute model](clarinute.svg)
*Block diagram of the clarinute model.  Adding a biquad filter after the jet delay and before the output, and converting the one-pole loss filter to a biquad would change this into the Whirlwind.*

## The Saxobowy

The STK's [Saxofony][saxofony] approximates the conical bore of the saxophone
with a waveguide excited partway along its length; this waveguide may be
interpreted as a cylindrical bore with the reed attached in the middle, or as a
string that is excited by a reed model.  Already a kind of hybrid model (a
blown string), the Saxofony model is structurally similar to a bowed string
model such as the [bowed][bowed] model in the STK, which also has an excitation
model that is connected to a waveguide partway along its length.  The similarity
of the two models seemed to suggest the opportunity to create a new hybrid.

After implementing both models in SOUL, I took a similar approach as that of
the clarinute, simply mixing the outputs of the two excitation models.  As
before, this was successful if not especially satisfying.  I found that I was
able to mix the two excitation models and still produce sound, but in general
the output had a tendency to be dominated by the behavior of the bow
excitation, as observed by the bowed-like spectrum output by the synthesizer.
Although I was able to evoke some novel sounds from the model, I'm uncertain
whether the same behaviors couldn't have been produced by the bowed string
model alone, and in general I found it quite finicky to work with the hybrid
model.

## Discussion

In general, the most satisfying aspects of the hybrid models came from
combining the linear-time-invariant parts of the models, particularly the
number and structure of delay lines, and changes to the filters such as the
crossfaded pole-zero lowpass filter used in the Blotar.  At some point I
switched to mainly using a one-pole lowpass with a dynamic pole, and found this
to be especially interesting, giving an effect similar to that of the filter in
a subtractive synthesizer.

Combining the excitation models proved more challenging, and I wasn't really
able to do this in a way that I found satisfying.  Particularly in the case of
the Saxobowy model, I had hoped to be able to produce a sound with an arbitrary
mix of harmonics between the more square-wave response of the reed model and
the more sawtooth-wave response of the bow model.  Evidently this could not be
achieved as easily as I thought, and I wasn't able to come anywhere close to
this ideal.  Unfortunately, the challenges ran even deeper than just an
inability to produce intermediary spectra from the combined excitation models
however.  In most cases it was difficult to produce any sound at all when
trying to combine two excitation methods.  

The difficulties encountered with combining the excitation models lead me to seek
better fundamental understanding of the excitation models themselves, which
lead me to the line of inquiry presented in the next section.

# Clarinet-like excitation

In order to better understand why my attempts to hybridize particularly the
excitation models of the various instruments incorporated into the Clarinute
and the Saxobowy, it became clear that I would first need to better understand
the operation of the original models.  The clarinet model is particularly
simple, consisting of a non-linearity coupled to a filter.  This is a kind of
dynamical system, and so I thought to consider the clarinet model using the
mathematics of non-linear dynamics.  Although my knowledge of this subject
remains limited, I was aware of key concepts such as fixed points, periodic
orbits, chaos, and Lyapunov exponents, as well as graphical tools such as
cobweb plots and bifurcation diagrams.

Applying these to the clarinet excitation (decoupled from the delay line and
loss filtering) with the breath pressure treated as the bifurcation parameter,
it was clearer how the model functions: the breath pressure, when raised past a
certain point, causes the dynamics of the model to change (bifurcate) from a
single fixed point (silence) to a period two orbit (sound).  Further increasing
the breath pressure causes the amplitude of the orbit to increase (causing an
increase in loudness), and then eventually (depending on the value of the reed
stiffness and opening parameters) the model reaches the overblown regime and
the periodic orbit is replaced by a fixed point.  When the non-linearity is
coupled to a delay line, the period two orbit becomes a period `N` orbit where
N is the length of the delay line.  The loss filter also doesn't seem to
significantly perturb the dynamics, instead simply softening the square wave
output by the non-linearity.

![Cobweb diagram of the STK clarinet non-linearity](clarinet_cobweb.gif)
*A cobweb diagram of the STK clarinet non-linearity animated with breath pressure increasing over time.  Notice the moment of bifurcation when the amplitude of the dynamics suddenly increases forming a period two orbit.*

Based on these observations, it seemed as though a much simpler model could be
employed to model the clarinet reed.  Any dynamic system with a period two
orbit should be sufficient.  I tested a few different models, present in the
repo as the squarinette1 and squarinette2 instruments.  Both of these use
clipping non-linearities with an adjustable slope parameter.  Increasing the
slope past one causes the dynamics to bifurcate into a stable period two orbit.

![Cobweb diagram of the squarinette1 non-linearity](squarinette1_cobweb.gif)
*A cobweb diagram of the squarinette1 non-linearity animated with slope increasing over time.  In this model the bifurcation happens very suddenly, and the orbit immediately reaches the maximum amplitude;  This translates to a poorer control of loudness in the model compared to the STK clarinet, although the spectrum is very similar.*

Noting the quadratic term in the clarinet non-linearity, I also thought to try
using a logistic map as the excitation model coupled to a delay line and a
filter.  This model (logistinette in the repo) is particularly interesting to
interact with since it exhibits period doubling and chaotic behaviours that
elicit new and unusual sounds.  This approach of coupling a chaotic map to a
waveguide has been explored in the literature e.g. by [Berdahl et al.][chaos
highway]

![Cobweb diagram of the logistic map](logistic_cobweb.gif)
*A cobweb diagram of the logistic map animated with the bifurcation parameter increasing from 3.0 to 4.0.  When coupled to a waveguide and lowpass filter, this results in an interesting synthesizer that produces a clarinet-like sound at low values of the bifurcation parameter.  As the parameter increases, interesting subharmonics and instabilities emerge, ultimately giving way to chaotic noise.*

Rodet and Vergez have published two papers ([1][rodet1], [2][rodet2]) providing a
more complete consideration of the non-linear dynamics of physical models.
This line of inquiry seems likely to offer a clearer path toward successful
hybrid excitation models.  Unfortunately, due to time limitations, a thorough
exploration of this path remains as future work.

# Conclusion

Combining unrelated physical models to create hybrid instruments offers the
possibility to evoke new and unusual sounds.  Although I was not able to
achieve this goal in the course of this project, my studies have deeply
enriched my understanding and appreciation for the subtleties of physical
modelling synthesis.  Furthermore, promising future work remains.  By better
understanding the non-linear dynamical behavior of physical modelling synthesis
algorithms, I believe the exciting opportunities suggested by hybrid physical
models remain attainable.

# Works cited

Perry Cook. 1992. [A Meta-Wind-Instrument Physical Model, and a Meta-Controller for Real-Time Performance Control][whirlwind]. *Proceedings of the International Computer Music Conference*. 

Van Stiefel, Dan Trueman, and Perry Cook. 2004. [Re-coupling: the uBlotar synthesis instrument and the sHowl speaker-feedback controller][blotar]. *Proceedings of the International Computer Music Conference*. 

Edgar Berdahl, Eric Sheffield, Andrew Pfalz, and Anthony T. Marasco. 2018. [Widening the Razor-Thin Edge of Chaos Into a Musical Highway: Connecting Chaotic Maps to Digital Waveguides][chaos highway]. *Proceedings of the International Conference on New Interfaces for Musical Expression*.

Xavier Rodet and Christophe Vergez. 1999. [Nonlinear dynamics in physical models: Simple feedback-loop systems and properties][rodet1]. *Computer Music Journal*, 23(3), 18–34. 

8avier Rodet and Christophe Vergez. 1999. [Nonlinear dynamics in physical models: From basic models to true musical-instrument models][rodet2]. *Computer Music Journal*, 23(3), 35–49.

[whirlwind]: http://hdl.handle.net/2027/spo.bbp2372.1992.072
[blotar]: http://hdl.handle.net/2027/spo.bbp2372.2004.084
[soul]: linkhere
[stk]: linkhere
[saxofony]: linkhere
[bowed]: linkhere
[soul announcement]: https://youtu.be/-GhleKNaPdk?t=909
[soul command line]: linkhere
[juce]: linkhere
[chaos highway]: https://www.nime.org/proceedings/2018/nime2018_paper0087.pdf
[rodet1]: https://www.mitpressjournals.org/doi/10.1162/014892699559869
[rodet2]: https://www.mitpressjournals.org/doi/abs/10.1162/014892699559878
