mod crds;

fn main() -> std::io::Result<()> {
    crds::microsoft_sentinel_detection_rule::write_crd().unwrap();
    Ok(())
}
