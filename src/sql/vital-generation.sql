CREATE index idx_path ON note USING btree (path collate "en_US" text_pattern_ops,ref_type_note,ref_etat_note);
