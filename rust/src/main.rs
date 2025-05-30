mod crds;

fn main() -> std::io::Result<()> {
    crds::microsoft_sentinel_analytic_rule::write_schemas().unwrap();
    crds::microsoft_sentinel_automation_rule::write_schemas().unwrap();
    crds::microsoft_sentinel_workbook::write_schemas().unwrap();
    crds::microsoft_sentinel_macro::write_schemas().unwrap();
    crds::splunk_detection_rule::write_schemas().unwrap();
    Ok(())
}
