create table if not exists public.model_parameters
(
    models_id          text
        constraint model_parameters_models_id_fk
            references public.models (id),
    temperature        real default 1.00 not null,
    top_p              real default 1.00 not null,
    top_k              real default 200  not null,
    frequency_penalty  real default 0.00 not null,
    presence_penalty   real default 0.00 not null,
    repetition_penalty real default 1.00 not null,
    min_p              real default 0.00 not null,
    top_a              real default 0.00 not null
);

comment on table public.model_parameters is 'Model Parameters for specific models';

comment on column public.model_parameters.temperature is 'Influences the variety of the model''s responses';

comment on column public.model_parameters.top_p is 'Limits the model''s choices to a percentage of likely tokens.';

comment on column public.model_parameters.top_k is 'Limits the model''s choice of tokens at each step.';

comment on column public.model_parameters.frequency_penalty is 'Penalizes the model for repeated tokens that appear often in the INPUT';

comment on column public.model_parameters.presence_penalty is 'Penalizes the model for repetition of tokens already present in the INPUT.';

comment on column public.model_parameters.repetition_penalty is 'Helps reduce the repetition of tokens from the input. Higher values can produce run-on sentences.';

comment on column public.model_parameters.min_p is 'The minimum probability of a token to be the next token relative to the most likely token.';

comment on column public.model_parameters.top_a is 'Consider on the top tokens with high enough probability to be the most likely next token. Like a"dynamic top_p".';

alter table public.model_parameters
    owner to postgres;