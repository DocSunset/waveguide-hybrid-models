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

TODO: figure here

Implementing the flute, electric guitar, and Blotar was reasonably
straightforward.  The flute model and the Blotar can be found in the
repository; the electric guitar implementation is omitted in the interest of
saving time and because it is only a very simple Karplus-Strong string model.

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
abandoned the brass model entirely, focusing instead on the Saxobowy.  The flute and clarinet implementations are available in the repository, as is the "clarinute" model that combines the two.

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



# Conclusion

# Works cited

[whirlwind]: linkhere
[blotar]: linkhere
[soul]: linkhere
[stk]: linkhere
[saxofony]: linkhere
[bowed]: linkhere
[soul announcement]: https://youtu.be/-GhleKNaPdk?t=909
[soul command line]: linkhere
[juce]: linkhere



[chaos highway]: linkhere
