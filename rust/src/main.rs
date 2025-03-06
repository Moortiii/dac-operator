mod crds;

fn main() -> std::io::Result<()> {
    crds::microsoft_sentinel_detection_rule::write_schemas().unwrap();
    crds::microsoft_sentinel_automation_rule::write_schemas().unwrap();
    crds::microsoft_sentinel_workbook::write_schemas().unwrap();
    crds::microsoft_sentinel_macro::write_schemas().unwrap();
    Ok(())
}
