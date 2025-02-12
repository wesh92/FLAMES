create table if not exists public.models
(
    id                          text                                                                                             not null
        constraint unique_id
            unique,
    object_type                 text          default 'model'::text not null,
    created_at                  timestamp     default CURRENT_TIMESTAMP                                                          not null,
    owned_by                    text          default 'state_of_tn'::text                                                        not null,
    local_path                  text,
    base_url_path               text          default 'https://openrouter.ai/api/v1'::text,
    model_path                  text generated always as (((lower(owned_by) || '/'::text) ||
                                                           lower(regexp_replace(id, '\s+'::text, '-'::text, 'g'::text)))) stored not null,
    available_roles             model_roles[] default ARRAY ['user'::model_roles, 'system'::model_roles, 'ai'::model_roles]      not null,
    max_input_token_window_size bigint,
    max_output_token_size       bigint,
    constraint models_pk
        primary key (id, object_type, owned_by, model_path)
);

comment on table public.models is 'Metadata About Models';

comment on column public.models.id is 'Human-friendly Model Name (eg. "R1 Distill Llama 70b")';

comment on column public.models.object_type is 'model type';

comment on column public.models.created_at is 'When the model or other type was created';

comment on column public.models.owned_by is 'Owning User or Org';

comment on column public.models.local_path is 'File Path to the Model if Local';

comment on column public.models.model_path is 'Semantic/Canonical Path for the mode (eg. "deepseek/deepseek-r1")';

comment on column public.models.available_roles is 'Role Types defined by the models that they will accept as actor types';

comment on column public.models.max_input_token_window_size is 'The input context window size of the model (including history, etc.)';

comment on column public.models.max_output_token_size is 'Maximum expected output size in tokens';

alter table public.models
    owner to postgres;

