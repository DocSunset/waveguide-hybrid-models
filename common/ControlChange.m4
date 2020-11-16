define(`forloop', `pushdef(`$1', `$2')_forloop($@)popdef(`$1')')
define(`_forloop',
       `$4`'ifelse($1, `$3', `', `define(`$1', incr($1))$0($@)')')
divert`'dnl

forloop(`__chan', `0', `15', `forloop(`__cc', `0', `15', `
processor CC_`'__chan`'_`'__cc
{
    input event soul::note_events::Control controlIn;
    output event float controlOut;

    event controlIn (soul::note_events::Control e)
    {
        if (e.control == __cc && e.channel == __chan)
            controlOut << e.value;
    }
}')')
