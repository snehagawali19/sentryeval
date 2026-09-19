def verify_metric(original, rerun, tolerance=1e-12):
    same = (
        original.provenance.dataset_version == rerun.provenance.dataset_version
        and original.provenance.judge_id == rerun.provenance.judge_id
        and original.provenance.metric_name == rerun.provenance.metric_name
    )
    return same and abs(original.raw_value - rerun.raw_value) <= tolerance
