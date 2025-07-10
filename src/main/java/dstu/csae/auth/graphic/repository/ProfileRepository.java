package dstu.csae.auth.graphic.repository;

import java.util.UUID;

import dstu.csae.auth.graphic.model.Profile;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ProfileRepository extends JpaRepository<Profile, UUID> {



}

