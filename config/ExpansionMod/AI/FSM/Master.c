class Expansion_Vehicles_GoToVehicle_State_0: ExpansionState_GoToVehicle {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GoToVehicle_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GoToVehicle_State_0";
		m_Name = "GoToVehicle";
	}
	override void OnEntry(string Event, ExpansionState From) {
		super.OnEntry(Event, From);
		entity = fsm.entity;
		seat = fsm.seat;
		super.OnEntry(Event, null);
		unit.OverrideMovementDirection(false, 0);
		unit.OverrideMovementSpeed(false, 0);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		super.OnExit(Event, Aborted, To);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (super.OnUpdate(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Vehicles_GetInVehicle_State_0: ExpansionState_GetInVehicle {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GetInVehicle_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GetInVehicle_State_0";
		m_Name = "GetInVehicle";
	}
	override void OnEntry(string Event, ExpansionState From) {
		super.OnEntry(Event, From);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		super.OnExit(Event, Aborted, To);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (super.OnUpdate(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Vehicles_GetOutVehicle_State_0: ExpansionState_GetOutVehicle {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GetOutVehicle_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GetOutVehicle_State_0";
		m_Name = "GetOutVehicle";
	}
	override void OnEntry(string Event, ExpansionState From) {
		super.OnEntry(Event, From);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		super.OnExit(Event, Aborted, To);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (super.OnUpdate(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Vehicles_OpenVehicleDoor_State_0: ExpansionState_OpenVehicleDoor {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_OpenVehicleDoor_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_OpenVehicleDoor_State_0";
		m_Name = "OpenVehicleDoor";
	}
	override void OnEntry(string Event, ExpansionState From) {
		super.OnEntry(Event, From);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		super.OnExit(Event, Aborted, To);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (super.OnUpdate(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Vehicles_CloseVehicleDoor_State_0: ExpansionState_CloseVehicleDoor {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_CloseVehicleDoor_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_CloseVehicleDoor_State_0";
		m_Name = "CloseVehicleDoor";
	}
	override void OnEntry(string Event, ExpansionState From) {
		super.OnEntry(Event, From);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		super.OnExit(Event, Aborted, To);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (super.OnUpdate(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Vehicles_Sitting_State_0: eAIState {
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_Sitting_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_Sitting_State_0";
		m_Name = "Sitting";
	}
	override void OnEntry(string Event, ExpansionState From) {
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		return EXIT;
	}
}
class Expansion_Vehicles_GoToVehicle_OpenVehicleDoor_Transition_0: eAITransition {
	private Expansion_Vehicles_GoToVehicle_State_0 src;
	private Expansion_Vehicles_OpenVehicleDoor_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GoToVehicle_OpenVehicleDoor_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GoToVehicle_OpenVehicleDoor_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_GoToVehicle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
	}
	override int Guard() {
		if (vector.Distance(unit.GetPosition(), src.position) > 0.5) return FAIL;
		if (!src.transport.IsAreaAtDoorFree(src.seat)) return FAIL;
		CarScript cs;
		if (src.transport.CrewMember(src.seat) || (Class.CastTo(cs, src.transport) && cs.Expansion_IsSeatReservedByOther(src.seat, unit))) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_GoToVehicle_GoToVehicle_Transition_0: eAITransition {
	private Expansion_Vehicles_GoToVehicle_State_0 src;
	private Expansion_Vehicles_GoToVehicle_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GoToVehicle_GoToVehicle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GoToVehicle_GoToVehicle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_GoToVehicle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_GoToVehicle_State_0"));
	}
	override int Guard() {
		if (vector.Distance(unit.GetPosition(), src.position) < 0.5) return FAIL;
		if (unit.GetThreatToSelf() > 0.4) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_OpenVehicleDoor_GetInVehicle_Transition_0: eAITransition {
	private Expansion_Vehicles_OpenVehicleDoor_State_0 src;
	private Expansion_Vehicles_GetInVehicle_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_OpenVehicleDoor_GetInVehicle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_OpenVehicleDoor_GetInVehicle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_GetInVehicle_State_0"));
	}
	override int Guard() {
		if (vector.Distance(unit.GetPosition(), src.position) > 0.5) return FAIL;
		if (unit.IsInTransport()) return FAIL;
		if (src.entity.IsKindOf("ExpansionBus")) return FAIL;  //! Hard block bus until seating CTD is fixed
		if (!src.transport.CrewCanGetThrough(src.seat) || !src.transport.IsAreaAtDoorFree(src.seat)) return FAIL;
		CarScript cs;
		if (src.transport.CrewMember(src.seat) || (Class.CastTo(cs, src.transport) && cs.Expansion_IsSeatReservedByOther(src.seat, unit))) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_GetInVehicle_CloseVehicleDoor_Transition_0: eAITransition {
	private Expansion_Vehicles_GetInVehicle_State_0 src;
	private Expansion_Vehicles_CloseVehicleDoor_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GetInVehicle_CloseVehicleDoor_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GetInVehicle_CloseVehicleDoor_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_GetInVehicle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_CloseVehicleDoor_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_Sitting_OpenVehicleDoor_Transition_0: eAITransition {
	private Expansion_Vehicles_Sitting_State_0 src;
	private Expansion_Vehicles_OpenVehicleDoor_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_Sitting_OpenVehicleDoor_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_Sitting_OpenVehicleDoor_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_Sitting_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
	}
	override int Guard() {
		auto group = unit.GetGroup();
		if (!group) return FAIL;
		auto leader = group.GetLeader();
		if (leader && leader != unit)
		{
			if (group.GetFormationState() != eAIGroupFormationState.IN || leader.GetParent() == unit.GetParent())
			return FAIL;
		}
		if (!dst.transport.IsAreaAtDoorFree(dst.seat)) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_OpenVehicleDoor_GetOutVehicle_Transition_0: eAITransition {
	private Expansion_Vehicles_OpenVehicleDoor_State_0 src;
	private Expansion_Vehicles_GetOutVehicle_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_OpenVehicleDoor_GetOutVehicle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_OpenVehicleDoor_GetOutVehicle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_GetOutVehicle_State_0"));
	}
	override int Guard() {
		if (!unit.IsInTransport()) return FAIL;
		if (!src.transport.CrewCanGetThrough(src.seat) || !src.transport.IsAreaAtDoorFree(src.seat)) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_GetOutVehicle_CloseVehicleDoor_Transition_0: eAITransition {
	private Expansion_Vehicles_GetOutVehicle_State_0 src;
	private Expansion_Vehicles_CloseVehicleDoor_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GetOutVehicle_CloseVehicleDoor_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GetOutVehicle_CloseVehicleDoor_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_GetOutVehicle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_CloseVehicleDoor_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_CloseVehicleDoor_Sitting_Transition_0: eAITransition {
	private Expansion_Vehicles_CloseVehicleDoor_State_0 src;
	private Expansion_Vehicles_Sitting_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_CloseVehicleDoor_Sitting_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_CloseVehicleDoor_Sitting_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_CloseVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_Sitting_State_0"));
	}
	override int Guard() {
		if (!unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_Sitting_Sitting_Transition_0: eAITransition {
	private Expansion_Vehicles_Sitting_State_0 src;
	private Expansion_Vehicles_Sitting_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_Sitting_Sitting_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_Sitting_Sitting_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_Sitting_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_Sitting_State_0"));
	}
	override int Guard() {
		if (!unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_OpenVehicleDoor_Sitting_Transition_0: eAITransition {
	private Expansion_Vehicles_OpenVehicleDoor_State_0 src;
	private Expansion_Vehicles_Sitting_State_0 dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_OpenVehicleDoor_Sitting_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_OpenVehicleDoor_Sitting_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Vehicles_Sitting_State_0"));
	}
	override int Guard() {
		if (!unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_CloseVehicleDoor__Transition_0: eAITransition {
	private Expansion_Vehicles_CloseVehicleDoor_State_0 src;
	private ExpansionState dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_CloseVehicleDoor__Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_CloseVehicleDoor__Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_CloseVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("ExpansionState"));
	}
	override int Guard() {
		if (unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_OpenVehicleDoor__Transition_0: eAITransition {
	private Expansion_Vehicles_OpenVehicleDoor_State_0 src;
	private ExpansionState dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_OpenVehicleDoor__Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_OpenVehicleDoor__Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_OpenVehicleDoor_State_0"));
		Class.CastTo(dst, _fsm.GetState("ExpansionState"));
	}
	override int Guard() {
		if (unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_GoToVehicle__Transition_0: eAITransition {
	private Expansion_Vehicles_GoToVehicle_State_0 src;
	private ExpansionState dst;
	Expansion_Vehicles_FSM_0 fsm;
	void Expansion_Vehicles_GoToVehicle__Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Vehicles_GoToVehicle__Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Vehicles_GoToVehicle_State_0"));
		Class.CastTo(dst, _fsm.GetState("ExpansionState"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Vehicles_FSM_0: eAIFSM {
	EntityAI entity;
	int seat;
	void Expansion_Vehicles_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
		m_Name = "Vehicles";
		m_DefaultState = "Expansion_Vehicles_GoToVehicle_State_0";
		Setup();
	}
	void Setup() {
		AddState(new Expansion_Vehicles_GoToVehicle_State_0(this));
		AddState(new Expansion_Vehicles_GetInVehicle_State_0(this));
		AddState(new Expansion_Vehicles_GetOutVehicle_State_0(this));
		AddState(new Expansion_Vehicles_OpenVehicleDoor_State_0(this));
		AddState(new Expansion_Vehicles_CloseVehicleDoor_State_0(this));
		AddState(new Expansion_Vehicles_Sitting_State_0(this));
		AddTransition(new Expansion_Vehicles_GoToVehicle_OpenVehicleDoor_Transition_0(this));
		AddTransition(new Expansion_Vehicles_GoToVehicle_GoToVehicle_Transition_0(this));
		AddTransition(new Expansion_Vehicles_OpenVehicleDoor_GetInVehicle_Transition_0(this));
		AddTransition(new Expansion_Vehicles_GetInVehicle_CloseVehicleDoor_Transition_0(this));
		AddTransition(new Expansion_Vehicles_Sitting_OpenVehicleDoor_Transition_0(this));
		AddTransition(new Expansion_Vehicles_OpenVehicleDoor_GetOutVehicle_Transition_0(this));
		AddTransition(new Expansion_Vehicles_GetOutVehicle_CloseVehicleDoor_Transition_0(this));
		AddTransition(new Expansion_Vehicles_CloseVehicleDoor_Sitting_Transition_0(this));
		AddTransition(new Expansion_Vehicles_Sitting_Sitting_Transition_0(this));
		AddTransition(new Expansion_Vehicles_OpenVehicleDoor_Sitting_Transition_0(this));
		AddTransition(new Expansion_Vehicles_CloseVehicleDoor__Transition_0(this));
		AddTransition(new Expansion_Vehicles_OpenVehicleDoor__Transition_0(this));
		AddTransition(new Expansion_Vehicles_GoToVehicle__Transition_0(this));
	}
}
ExpansionFSM Create_Expansion_Vehicles_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
	return new Expansion_Vehicles_FSM_0(owner, parentState);
}
class Expansion_Fighting_Positioning_State_0: eAIState {
	Expansion_Fighting_FSM_0 fsm;
	vector position;
	float time;
	float movementDirection;
	void Expansion_Fighting_Positioning_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting_Positioning_State_0";
		m_Name = "Positioning";
	}
	override void OnEntry(string Event, ExpansionState From) {
		time = 0;
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		unit.OverrideMovementDirection(false, 0);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.eAI_IsChangingStance())
		return CONTINUE;
		bool wantsLower = false;
		bool wantsRaise = false;
		int timeSinceLastFire = GetGame().GetTime() - fsm.LastFireTime;
		if (fsm.LastFireTime > 0 && timeSinceLastFire > fsm.TimeBetweenFiring)
		{
			wantsLower = true;
		}
		auto target = unit.GetTarget();
		if (target)
		{
			position = target.GetPosition(unit, false);
			auto aimPosition = position + target.GetAimOffset(unit);
			fsm.DistanceToTargetSq = target.GetDistanceSq(unit, true);
			bool shouldBeMeleeing = false;
			auto hands = unit.GetHumanInventory().GetEntityInHands();
			bool isItemTarget = target.GetEntity().IsInherited(ItemBase);
			if (isItemTarget)
			{
				wantsLower = true;
			}
			else if (!hands)
			{
				shouldBeMeleeing = true;
			}
			else if (hands.IsWeapon())
			{
				if (fsm.DistanceToTargetSq <= 2.25)
				{
					shouldBeMeleeing = true;
				}
			}
			else if (hands.IsMeleeWeapon())
			{
				shouldBeMeleeing = true;
			}
			if (shouldBeMeleeing)
			{
				if (fsm.DistanceToTargetSq <= 3.24)
				{
					wantsRaise = true;
				}
				else
				{
					wantsLower = true;
				}
			}
			float minDist = 1.0;
			auto player = PlayerBase.Cast(target.GetEntity());
			if (player && player.IsUnconscious())
			minDist = 4.0;
			if (!isItemTarget && fsm.DistanceToTargetSq <= minDist)
			{
				time += DeltaTime;
				if (!movementDirection || time > Math.RandomIntInclusive(1, 3))
				{
					if (Math.RandomIntInclusive(0, 1))
					movementDirection = Math.RandomFloat(135, 180);
					else
					movementDirection = Math.RandomFloat(-135, -180);
				}
				unit.OverrideMovementDirection(true, movementDirection);
				unit.OverrideMovementSpeed(true, Math.RandomIntInclusive(1, 2));
			}
			else
			{
				unit.OverrideMovementDirection(false, 0);
				unit.OverrideMovementSpeed(false, 0);
				time = 0;
				movementDirection = 0;
			}
			unit.LookAtPosition(aimPosition);
			unit.AimAtPosition(aimPosition);
			unit.OverrideTargetPosition(position);
			if (hands && (hands.IsWeapon() || fsm.DistanceToTargetSq <= 100.0))
			{
				if (hands.HasEnergyManager() && !hands.GetCompEM().IsWorking() && hands.GetCompEM().CanSwitchOn())
				{
					hands.GetCompEM().SwitchOn();
				}
			}
		}
		else
		{
			unit.OverrideMovementDirection(false, 0);
			unit.OverrideMovementSpeed(false, 0);
			unit.OverrideTargetPosition(unit.GetPosition());
		}
		if (wantsRaise && unit.CanRaiseWeapon())
		{
			unit.RaiseWeapon(true);
		}
		else if (wantsLower || !unit.CanRaiseWeapon() || !unit.eAI_HasLOS())
		{
			unit.RaiseWeapon(false);
			unit.eAI_AdjustStance(fsm.LastFireTime, timeSinceLastFire, fsm.TimeBetweenFiringAndGettingUp);
		}
		return EXIT;
	}
}
class Expansion_Fighting_Evade_State_0: eAIState {
	Expansion_Fighting_FSM_0 fsm;
	void Expansion_Fighting_Evade_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting_Evade_State_0";
		m_Name = "Evade";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.eAI_ForceSideStep(1.0);
		unit.OverrideMovementSpeed(true, 3);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		unit.OverrideMovementSpeed(false, 0);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.eAI_IsSideStepping())
		return CONTINUE;
		return EXIT;
	}
}
class Expansion_Fighting_FireWeapon_State_0: eAIState {
	Expansion_Fighting_FSM_0 fsm;
	float time;
	eAITarget target;
	Weapon_Base weapon;
	void Expansion_Fighting_FireWeapon_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting_FireWeapon_State_0";
		m_Name = "FireWeapon";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.RaiseWeapon(true);
		time = 0;
		fsm.LastFireTime = GetGame().GetTime();
		if (unit.eAI_AdjustStance(weapon, fsm.DistanceToTargetSq))
		EXTrace.Print(EXTrace.AI, unit, "eAI_AdjustStance " + typename.EnumToString(eAIStance, unit.eAI_GetStance()));
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.eAI_IsChangingStance())
		return CONTINUE;
		if (!target)
		return EXIT;
		auto lowPosition = target.GetPosition(unit, false);
		auto aimPosition = lowPosition + target.GetAimOffset(unit);
		time += DeltaTime;
		unit.OverrideTargetPosition(lowPosition);
		unit.LookAtPosition(aimPosition);
		unit.AimAtPosition(aimPosition);
		if (!unit.IsRaised() || !unit.IsWeaponRaiseCompleted())
		{
			unit.RaiseWeapon(true);
			if (time >= 0.5)
			{
				return EXIT;
			}
			// waiting for the weapon to be raised
			return CONTINUE;
		}
		auto neck = unit.GetBonePositionWS(unit.GetBoneIndexByName("neck"));
		auto direction = vector.Direction(neck, aimPosition).Normalized();
		if (vector.Dot(unit.GetAimDirection(), direction) < 0.75)
		{
			if (time >= 0.5)
			{
				return EXIT;
			}
			// waiting for unit to face target
			return CONTINUE;
		}
		unit.TryFireWeapon();
		return EXIT;
	}
}
class Expansion_Fighting_Melee_State_0: eAIState {
	Expansion_Fighting_FSM_0 fsm;
	float time;
	eAITarget target;
	float movementDirection;
	void Expansion_Fighting_Melee_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting_Melee_State_0";
		m_Name = "Melee";
	}
	override void OnEntry(string Event, ExpansionState From) {
		time = 0;
		fsm.LastFireTime = GetGame().GetTime();
		unit.Expansion_GetUp();
		//! FIXME: Pistols fuck up the hand animation state.
		//! Ugly workaround: Put away when entering melee.
		auto hands = unit.GetItemInHands();
		if (hands && hands.IsKindOf("Pistol_Base"))
		{
			unit.eAI_TakeItemToInventory(hands);
		}
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		unit.OverrideMovementDirection(false, 0);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.eAI_IsChangingStance())
		return CONTINUE;
		if (!target)
		return EXIT;
		auto aimOffset = target.GetAimOffset(unit);
		auto lowPosition = target.GetPosition(unit, false);
		auto aimPosition = lowPosition + aimOffset;
		time += DeltaTime;
		unit.OverrideTargetPosition(lowPosition);
		unit.LookAtPosition(aimPosition);
		unit.AimAtPosition(aimPosition);
		fsm.DistanceToTargetSq = target.GetDistanceSq(unit, true);
		if (fsm.DistanceToTargetSq > 2.25)
		{
			if (time >= 0.5)
			{
				time = 0;
				return EXIT;
			}
			return CONTINUE;
		}
		auto direction = vector.Direction(unit.GetPosition(), lowPosition).Normalized();
		if (vector.Dot(unit.GetDirection(), direction) < 0.97)
		{
			if (time >= Math.RandomIntInclusive(1, 3))
			{
				unit.OverrideMovementDirection(false, 0);
				unit.OverrideMovementSpeed(false, 0);
				time = 0;
				movementDirection = 0;
				return EXIT;
			}
			if (!movementDirection || time > Math.RandomIntInclusive(1, 3))
			{
				if (Math.RandomIntInclusive(0, 1))
				movementDirection = Math.RandomFloat(135, 180);
				else
				movementDirection = Math.RandomFloat(-135, -180);
			}
			unit.OverrideMovementDirection(true, movementDirection);
			unit.OverrideMovementSpeed(true, Math.RandomIntInclusive(1, 2));
			return CONTINUE;
		}
		if (unit.IsFighting() && time < 0.3)
		{
			return CONTINUE;
		}
		unit.Notify_Melee();
		time = 0;
		movementDirection = 0;
		return EXIT;
	}
}
class Expansion_Fighting__Melee_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Fighting_Melee_State_0 dst;
	Expansion_Fighting_FSM_0 fsm;
	void Expansion_Fighting__Melee_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting__Melee_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Fighting_Melee_State_0"));
	}
	override int Guard() {
		if (unit.IsRestrained()) return FAIL;
		if (!unit.CanRaiseWeapon() || !unit.eAI_HasLOS()) return FAIL;
		// we are targetting an entity?
		dst.target = unit.GetTarget();
		if (!dst.target || !dst.target.IsMeleeViable(unit) || dst.target.GetThreat(unit) < 0.4) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Fighting__Evade_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Fighting_Evade_State_0 dst;
	Expansion_Fighting_FSM_0 fsm;
	void Expansion_Fighting__Evade_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting__Evade_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Fighting_Evade_State_0"));
	}
	override int Guard() {
		int missionTime = GetGame().GetTime();
		if (missionTime - fsm.LastEvadeTime < Math.RandomInt(2500, 5000)) return FAIL;
		auto target = unit.GetTarget();
		if (!target) return FAIL;
		auto targetPlayer = DayZPlayerImplement.Cast(target.GetEntity());
		if (!targetPlayer) return FAIL;
		if (!targetPlayer.IsRaised()) return FAIL;  //! Ignore if target player isn't raised
		if (!unit.eAI_HasLOS()) return FAIL;
		auto weapon = Weapon_Base.Cast(targetPlayer.GetHumanInventory().GetEntityInHands());
		if (!weapon) return FAIL;  //! Ignore if target player doesn't have a firearm
		vector fromTargetDirection = vector.Direction(targetPlayer.GetPosition(), unit.GetPosition()).Normalized();
		float fromTargetDot = vector.Dot(targetPlayer.Expansion_GetAimDirection(), fromTargetDirection);
		if (fromTargetDot < 0.97) return FAIL;  //! Ignore if target player isn't aiming at us
		if (Math.RandomInt(0, 5) > 0) return FAIL;  //! 1 in 5 chance to evade
		fsm.LastEvadeTime = missionTime;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Fighting__FireWeapon_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Fighting_FireWeapon_State_0 dst;
	Expansion_Fighting_FSM_0 fsm;
	void Expansion_Fighting__FireWeapon_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting__FireWeapon_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Fighting_FireWeapon_State_0"));
	}
	override int Guard() {
		if (unit.IsRestrained()) return FAIL;
		// we are aiming at something?
		dst.target = unit.GetTarget();
		if (!dst.target) return FAIL;
		PlayerBase player;
		ItemBase itemTarget;
		if (Class.CastTo(player, dst.target.GetEntity()))
		{
			if (player.IsUnconscious())
			return FAIL;
		}
		else if (Class.CastTo(itemTarget, dst.target.GetEntity()))
		{
			// don't shoot at bandages or ammo/magazines, silly
			if (itemTarget.Expansion_CanBeUsedToBandage())
			return FAIL;
			if (itemTarget.IsMagazine())
			return FAIL;
		}
		if (unit.IsFighting()) return FAIL;
		if (!Class.CastTo(dst.weapon, unit.GetItemInHands()) || dst.weapon.IsDamageDestroyed()) return FAIL;
		if (!unit.CanRaiseWeapon() || !unit.eAI_HasLOS()) return FAIL;
		if (!dst.weapon.Expansion_IsChambered()) return FAIL;
		if (unit.GetWeaponManager().CanUnjam(dst.weapon)) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Fighting__Positioning_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Fighting_Positioning_State_0 dst;
	Expansion_Fighting_FSM_0 fsm;
	void Expansion_Fighting__Positioning_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Fighting__Positioning_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Fighting_Positioning_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Fighting_FSM_0: eAIFSM {
	int LastFireTime;
	int TimeBetweenFiring = 5000;
	int TimeBetweenFiringAndGettingUp = 15000;
	int LastEvadeTime;
	float DistanceToTargetSq;
	void Expansion_Fighting_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
		m_Name = "Fighting";
		m_DefaultState = "Expansion_Fighting_Positioning_State_0";
		Setup();
	}
	void Setup() {
		AddState(new Expansion_Fighting_Positioning_State_0(this));
		AddState(new Expansion_Fighting_Evade_State_0(this));
		AddState(new Expansion_Fighting_FireWeapon_State_0(this));
		AddState(new Expansion_Fighting_Melee_State_0(this));
		AddTransition(new Expansion_Fighting__Melee_Transition_0(this));
		AddTransition(new Expansion_Fighting__Evade_Transition_0(this));
		AddTransition(new Expansion_Fighting__FireWeapon_Transition_0(this));
		AddTransition(new Expansion_Fighting__Positioning_Transition_0(this));
	}
}
ExpansionFSM Create_Expansion_Fighting_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
	return new Expansion_Fighting_FSM_0(owner, parentState);
}
class Expansion_Reloading_Start_State_0: eAIState {
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Start_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Start_State_0";
		m_Name = "Start";
	}
	override void OnEntry(string Event, ExpansionState From) {
		fsm.last_attempt_time = GetGame().GetTime();
		unit.OverrideMovementSpeed(false, 0);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		return EXIT;
	}
}
class Expansion_Reloading_Reloading_State_0: eAIState {
	Expansion_Reloading_FSM_0 fsm;
	Magazine magazine;
	float time;
	void Expansion_Reloading_Reloading_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Reloading_State_0";
		m_Name = "Reloading";
	}
	override void OnEntry(string Event, ExpansionState From) {
		time = 0;
		unit.RaiseWeapon(false);
		unit.ReloadWeaponAI(fsm.weapon, magazine);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		unit.eAI_CancelSidestep();
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!unit.GetWeaponManager() || unit.IsUnconscious()) return EXIT;
		if (unit.GetWeaponManager().IsRunning())
		{
			time += DeltaTime;
			if (time > 12)  //! Looks like something went terribly wrong
			{
				EXTrace.Print(true, unit, "Weapon_Reloading - Reloading - timeout");
				unit.eAI_Unbug("reload");
				return EXIT;
			}
			vector position;
			auto target = unit.GetTarget();
			if (target && unit.GetThreatToSelf() > 0.4)
			{
				if (!unit.eAI_IsSideStepping() && unit.eAI_HasLOS())
				{
					float distSq = target.GetDistanceSq(unit, true);
					if (distSq <= 2.25)
					{
						float movementDirection;
						if (Math.RandomIntInclusive(0, 1))
						movementDirection = Math.RandomFloat(135, 180);
						else
						movementDirection = Math.RandomFloat(-135, -180);
						unit.eAI_ForceSideStep(Math.RandomFloat(1, 1.5), null, movementDirection);
					}
					else if (distSq < 100.0)
					{
						unit.eAI_ForceSideStep(Math.RandomFloat(1, 1.5), null, 0.0, false);
					}
				}
				position = target.GetPosition(unit, false);
			}
			else
			{
				auto group = unit.GetGroup();
				if (group)
				{
					if (group.GetLeader() != unit)
					position = group.GetFormationPosition(unit);
					else
					position = group.GetCurrentWaypoint();
				}
			}
			if (position != vector.Zero)
			unit.OverrideTargetPosition(position);
			return CONTINUE;
		}
		if (!fsm.weapon) return EXIT;
		if (fsm.weapon.IsDamageDestroyed())
		{
			unit.eAI_DropItem(fsm.weapon);
		}
		else if (fsm.weapon.IsChamberEmpty(fsm.weapon.GetCurrentMuzzle()))
		{
			fsm.failed_attempts++;
			EXTrace.Print(true, unit, "Weapon_Reloading - Reloading - failed (" + fsm.failed_attempts + ")");
			fsm.weapon.ValidateAndRepair();
		}
		else
		{
			fsm.failed_attempts = 0;
		}
		return EXIT;
	}
}
class Expansion_Reloading_Reloading_Fail_State_0: eAIState {
	Expansion_Reloading_FSM_0 fsm;
	float time;
	void Expansion_Reloading_Reloading_Fail_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Reloading_Fail_State_0";
		m_Name = "Reloading_Fail";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.RaiseWeapon(false);
		time = 0;
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		time += DeltaTime;
		// waiting for the weapon to be lowered
		if (fsm.weapon && time < 0.5)
		return CONTINUE;
		return EXIT;
	}
}
class Expansion_Reloading_Removing_State_0: eAIState {
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Removing_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Removing_State_0";
		m_Name = "Removing";
	}
	override void OnEntry(string Event, ExpansionState From) {
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!fsm.weapon || unit.GetItemInHands() != fsm.weapon)
		return EXIT;  // remove complete
		if (!unit.eAI_TakeItemToInventory(fsm.weapon))
		unit.eAI_DropItem(fsm.weapon);
		return CONTINUE;
	}
}
class Expansion_Reloading_Start_Reloading_Transition_0: eAITransition {
	private Expansion_Reloading_Start_State_0 src;
	private Expansion_Reloading_Reloading_State_0 dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Start_Reloading_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Start_Reloading_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Reloading_Start_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Reloading_Reloading_State_0"));
	}
	override int Guard() {
		if (!fsm.weapon || fsm.weapon.IsDamageDestroyed())
		return FAIL;
		if (!unit.eAI_HasAmmoForFirearm(fsm.weapon, dst.magazine)) return FAIL;
		if (!dst.magazine)
		EXTrace.Start0(EXTrace.AI, this, "Reloading " + fsm.weapon + " from internal mag");
		else
		EXTrace.Start0(EXTrace.AI, this, "Reloading " + fsm.weapon + " from mag " + dst.magazine);
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading_Start_Reloading_Fail_Transition_0: eAITransition {
	private Expansion_Reloading_Start_State_0 src;
	private Expansion_Reloading_Reloading_Fail_State_0 dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Start_Reloading_Fail_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Start_Reloading_Fail_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Reloading_Start_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Reloading_Reloading_Fail_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading_Reloading_Fail_Removing_Transition_0: eAITransition {
	private Expansion_Reloading_Reloading_Fail_State_0 src;
	private Expansion_Reloading_Removing_State_0 dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Reloading_Fail_Removing_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Reloading_Fail_Removing_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Reloading_Reloading_Fail_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Reloading_Removing_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading_Reloading__Transition_0: eAITransition {
	private Expansion_Reloading_Reloading_State_0 src;
	private ExpansionState dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Reloading__Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Reloading__Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Reloading_Reloading_State_0"));
		Class.CastTo(dst, _fsm.GetState("ExpansionState"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading_Removing__Transition_0: eAITransition {
	private Expansion_Reloading_Removing_State_0 src;
	private ExpansionState dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading_Removing__Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading_Removing__Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Reloading_Removing_State_0"));
		Class.CastTo(dst, _fsm.GetState("ExpansionState"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading__Start_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Reloading_Start_State_0 dst;
	Expansion_Reloading_FSM_0 fsm;
	void Expansion_Reloading__Start_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Reloading__Start_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Reloading_Start_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Reloading_FSM_0: eAIFSM {
	Weapon_Base weapon;
	int last_attempt_time;
	int failed_attempts;
	void Expansion_Reloading_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
		m_Name = "Reloading";
		m_DefaultState = "Expansion_Reloading_Start_State_0";
		Setup();
	}
	void Setup() {
		AddState(new Expansion_Reloading_Start_State_0(this));
		AddState(new Expansion_Reloading_Reloading_State_0(this));
		AddState(new Expansion_Reloading_Reloading_Fail_State_0(this));
		AddState(new Expansion_Reloading_Removing_State_0(this));
		AddTransition(new Expansion_Reloading_Start_Reloading_Transition_0(this));
		AddTransition(new Expansion_Reloading_Start_Reloading_Fail_Transition_0(this));
		AddTransition(new Expansion_Reloading_Reloading_Fail_Removing_Transition_0(this));
		AddTransition(new Expansion_Reloading_Reloading__Transition_0(this));
		AddTransition(new Expansion_Reloading_Removing__Transition_0(this));
		AddTransition(new Expansion_Reloading__Start_Transition_0(this));
	}
}
ExpansionFSM Create_Expansion_Reloading_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
	return new Expansion_Reloading_FSM_0(owner, parentState);
}
class Expansion_Master_Idle_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Idle_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Idle_State_0";
		m_Name = "Idle";
	}
	override void OnEntry(string Event, ExpansionState From) {
		if (!unit.GetTarget())
		{
			if (unit.GetLookDirectionRecalculate())
			unit.LookAtDirection("0 0 1");
			if (unit.GetAimDirectionRecalculate())
			unit.AimAtDirection("0 0 1");
		}
		auto hands = unit.GetItemInHands();
		if (hands && hands.HasEnergyManager() && hands.GetCompEM().IsWorking() && hands.GetCompEM().CanSwitchOff())
		{
			hands.GetCompEM().SwitchOff();
		}
		unit.OverrideMovementDirection(false, 0);
		unit.OverrideMovementSpeed(true, 0);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		return EXIT;
	}
}
class Expansion_Master_Unconscious_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	float time;
	void Expansion_Master_Unconscious_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Unconscious_State_0";
		m_Name = "Unconscious";
	}
	override void OnEntry(string Event, ExpansionState From) {
		time = 0;
		unit.OverrideTargetPosition(unit.GetPosition());
		unit.OverrideMovementSpeed(true, 0);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (time > 3)
		{
			return EXIT;
		}
		if (!unit.IsUnconscious())
		{
			time += DeltaTime;  //! Allow time to stand up so we don't instantly start firing
		}
		return CONTINUE;
	}
}
class Expansion_Master_Interacting_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Interacting_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Interacting_State_0";
		m_Name = "Interacting";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.OverrideTargetPosition(unit.GetPosition() + unit.GetDirection() * unit.Expansion_GetMovementSpeed());
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.eAI_HasInteractingPlayers())
		{
			return CONTINUE;
		}
		return EXIT;
	}
}
class Expansion_Master_FollowFormation_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	eAIGroup group;
	int speedLimit;
	void Expansion_Master_FollowFormation_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_FollowFormation_State_0";
		m_Name = "FollowFormation";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.Expansion_GetUp();
		unit.OverrideMovementDirection(false, 0);
		unit.OverrideMovementSpeed(false, 0);
		speedLimit = unit.GetMovementSpeedLimit();
		if (speedLimit > 0)
		unit.SetMovementSpeedLimit(3);  //! Make sure AI can reach formation positions when following leader by overriding speed limit
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		if (speedLimit > 0)
		unit.SetMovementSpeedLimit(speedLimit);  //! Restore speed limit
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!group) return EXIT;
		unit.OverrideTargetPosition(group.GetFormationPosition(unit));
		return EXIT;
	}
}
class Expansion_Master_TraversingWaypoints_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	ref TVectorArray path;
	eAIWaypointBehavior behaviour;
	bool backtracking;
	int index;
	float threshold = 1.0;
	float previousDistance;
	vector previousWayPoint;
	void Expansion_Master_TraversingWaypoints_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TraversingWaypoints_State_0";
		m_Name = "TraversingWaypoints";
	}
	override void OnEntry(string Event, ExpansionState From) {
		path = unit.GetGroup().GetWaypoints();
		if (path.Count() == 0)
		{
			path = { unit.GetPosition() + unit.GetDirection() * unit.Expansion_GetMovementSpeed() };
		}
		behaviour = unit.GetGroup().GetWaypointBehaviour();
		unit.Expansion_GetUp();
		if (previousWayPoint == vector.Zero && path.Count() > 1)
		previousWayPoint = path[0] - vector.Direction(path[0], path[1]).Normalized();
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (behaviour == eAIWaypointBehavior.HALT)
		return EXIT;
		index = unit.GetGroup().m_CurrentWaypointIndex;
		backtracking = unit.GetGroup().m_BackTracking;
		float distance = vector.DistanceSq(unit.GetPosition(), path[index]);
		if (distance < threshold)
		{
			previousWayPoint = path[index];
			if (backtracking) index--;
			else index++;
			threshold = 1.0;
		}
		else if (Math.AbsFloat(distance - previousDistance) < 0.0016)
		{
			//! We seem to not be getting closer to the waypoint, possibly the path is blocked.
			//! Increase threshold until we are within distance.
			threshold += 0.01;
		}
		previousDistance = distance;
		if (index < 0)
		{
			if (behaviour == eAIWaypointBehavior.ALTERNATE)
			{
				backtracking = false;
				index = 1;
			}
			else
			{
				index = path.Count() - 1;
			}
		}
		else if (index == path.Count())
		{
			if (behaviour == eAIWaypointBehavior.ALTERNATE)
			{
				backtracking = true;
				index = path.Count() - 2;
			}
			else if (behaviour == eAIWaypointBehavior.LOOP)
			{
				index = 0;
			}
		}
		index = Math.Clamp(index, 0, path.Count() - 1);
		bool isFinal;
		if (behaviour != eAIWaypointBehavior.LOOP)
		isFinal = index == 0 || index == path.Count() - 1;
		unit.OverrideTargetPosition(path[index], isFinal);
		unit.OverrideMovementDirection(false, 0);
		unit.OverrideMovementSpeed(false, 0);
		vector direction;
		if (path.Count() > 1)
		direction = vector.Direction(previousWayPoint, path[index]).Normalized();
		else
		direction = unit.GetDirection();
		unit.Expansion_DebugObject_Deferred(index + 20, path[index] - "0 1.5 0", "ExpansionDebugNoticeMe_Red", direction);
		unit.Expansion_DebugObject_Deferred(path.Count() + 20, path[index], "ExpansionDebugNoticeMe", unit.GetDirection());
		unit.GetGroup().m_CurrentWaypointIndex = index;
		unit.GetGroup().m_BackTracking = backtracking;
		return EXIT;
	}
}
class Expansion_Master_Vehicles_State_0: eAIState {
	Expansion_Vehicles_FSM_0 sub_fsm;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Vehicles_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Vehicles_State_0";
		m_Name = "Vehicles";
		m_SubFSM = new Expansion_Vehicles_FSM_0(_fsm.GetOwner(), this);
		Class.CastTo(sub_fsm, m_SubFSM);
	}
	override void OnEntry(string Event, ExpansionState From) {
		if (Event != "") m_SubFSM.Start(Event);
		else m_SubFSM.StartDefault();
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		if (Aborted) m_SubFSM.Abort(Event);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (m_SubFSM.Update(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		auto group = unit.GetGroup();
		if (!group) return EXIT;
		auto leader = group.GetLeader();
		//! @note leader can only briefly be null (disconnected/killed).
		//! We wait until a new leader has been determined (which may be the current unit).
		if (!leader) return CONTINUE;
		if (!sub_fsm.entity) return EXIT;
		if ((leader != unit && leader.IsInTransport() && leader.GetParent() == sub_fsm.entity) || unit.IsInTransport()) return CONTINUE;
		//! Wait until AI has left the vehicle and closed the door (if any)
		bool hasDoor;
		string source;
		ExpansionFSMHelper.DoorAnimationSource(sub_fsm.entity, sub_fsm.seat, hasDoor, source);
		if (hasDoor && sub_fsm.entity.GetAnimationPhase(source) > 0.5) return CONTINUE;
		return EXIT;
	}
}
class Expansion_Master_Fighting_State_0: eAIState {
	Expansion_Fighting_FSM_0 sub_fsm;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Fighting_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Fighting_State_0";
		m_Name = "Fighting";
		m_SubFSM = new Expansion_Fighting_FSM_0(_fsm.GetOwner(), this);
		Class.CastTo(sub_fsm, m_SubFSM);
	}
	override void OnEntry(string Event, ExpansionState From) {
		if (Event != "") m_SubFSM.Start(Event);
		else m_SubFSM.StartDefault();
		if (unit.GetEmoteManager().IsEmotePlaying())
		unit.GetEmoteManager().ServerRequestEmoteCancel();
		unit.eAI_SetIsFightingFSM(true);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		if (Aborted) m_SubFSM.Abort(Event);
		unit.eAI_SetIsFightingFSM(false);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (m_SubFSM.Update(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return EXIT;
	}
}
class Expansion_Master_Weapon_Reloading_State_0: eAIState {
	Expansion_Reloading_FSM_0 sub_fsm;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Weapon_Reloading_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Weapon_Reloading_State_0";
		m_Name = "Reloading";
		m_SubFSM = new Expansion_Reloading_FSM_0(_fsm.GetOwner(), this);
		Class.CastTo(sub_fsm, m_SubFSM);
	}
	override void OnEntry(string Event, ExpansionState From) {
		if (Event != "") m_SubFSM.Start(Event);
		else m_SubFSM.StartDefault();
		if (unit.GetEmoteManager().IsEmotePlaying())
		unit.GetEmoteManager().ServerRequestEmoteCancel();
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		if (Aborted) m_SubFSM.Abort(Event);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (m_SubFSM.Update(DeltaTime, SimulationPrecision) == EXIT) return EXIT;
		return CONTINUE;
	}
}
class Expansion_Master_Weapon_Unjamming_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	Weapon_Base weapon;
	float time;
	int failed_attempts;
	void Expansion_Master_Weapon_Unjamming_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Weapon_Unjamming_State_0";
		m_Name = "Weapon_Unjamming";
	}
	override void OnEntry(string Event, ExpansionState From) {
		time = 0;
		unit.RaiseWeapon(false);
		unit.StartActionObject(eAIActionWeaponUnjam, null);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		unit.OverrideMovementDirection(false, 0);
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!unit.GetWeaponManager() || unit.IsUnconscious()) return EXIT;
		if (unit.GetWeaponManager().IsRunning())
		{
			time += DeltaTime;
			if (time > 10)  //! Looks like something went terribly wrong
			{
				EXTrace.Print(true, unit, "Weapon_Unjamming - timeout");
				unit.eAI_Unbug("unjam");
				return EXIT;
			}
			auto target = unit.GetTarget();
			if (target && target.GetDistanceSq(unit, true) <= 2.25)
			{
				unit.OverrideMovementDirection(true, -180);
			}
			return CONTINUE;
		}
		if (unit.GetWeaponManager().CanUnjam(weapon))
		{
			failed_attempts++;
			EXTrace.Print(true, unit, "Weapon_Unjamming - failed (" + failed_attempts + ")");
			weapon.ValidateAndRepair();
		}
		else
		{
			failed_attempts = 0;
		}
		return EXIT;
	}
}
class Expansion_Master_TakeItemToHands_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	ItemBase item;
	float time;
	void Expansion_Master_TakeItemToHands_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TakeItemToHands_State_0";
		m_Name = "TakeItemToHands";
	}
	override void OnEntry(string Event, ExpansionState From) {
		EXTrace.Print(EXTrace.AI, unit, "TakeItemToHands " + item.ToString());
		time = 0;
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!item)
		return EXIT;
		if (unit.GetItemInHands() != item)
		{
			if (item.Expansion_IsInventoryLocked())
			ExpansionStatic.UnlockInventoryRecursive(item, 10134);
			if (!unit.eAI_TakeItemToHands(item))
			return EXIT;
		}
		if (time < 0.5)
		{
			time += DeltaTime;
			return CONTINUE;
		}
		return EXIT;
	}
}
class Expansion_Master_TakeItemToInventory_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	ItemBase item;
	float time;
	void Expansion_Master_TakeItemToInventory_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TakeItemToInventory_State_0";
		m_Name = "TakeItemToInventory";
	}
	override void OnEntry(string Event, ExpansionState From) {
		EXTrace.Print(EXTrace.AI, unit, "TakeItemToInventory " + item.ToString());
		time = 0;
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (!item)
		return EXIT;
		if (!item.GetHierarchyRootPlayer())
		{
			if (item.Expansion_IsInventoryLocked())
			ExpansionStatic.UnlockInventoryRecursive(item, 10134);
			if (!unit.eAI_TakeItemToInventory(item))
			return EXIT;
		}
		if (time < 0.5)
		{
			time += DeltaTime;
			return CONTINUE;
		}
		return EXIT;
	}
}
class Expansion_Master_Bandaging_Self_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	int last_bandage_attempt_time;
	ItemBase bandage;
	float timeout;
	float time;
	void Expansion_Master_Bandaging_Self_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Bandaging_Self_State_0";
		m_Name = "Bandaging_Self";
	}
	override void OnEntry(string Event, ExpansionState From) {
		last_bandage_attempt_time = GetGame().GetTime();
		time = 0;
		float effectivity = bandage.GetBandagingEffectivity();
		if (effectivity > 0)
		timeout = UATimeSpent.BANDAGE / effectivity + 8.0;
		else
		timeout = 16.0;
		if (unit.IsPlayerInStance(DayZPlayerConstants.STANCEMASK_PRONE | DayZPlayerConstants.STANCEMASK_RAISEDPRONE))
		unit.OverrideStance(DayZPlayerConstants.STANCEIDX_CROUCH);
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
		if (bandage)
		{
			if (bandage.IsDamageDestroyed() || !unit.eAI_TakeItemToInventory(bandage))
			{
				unit.eAI_DropItem(bandage);
			}
		}
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		if (unit.IsUnconscious()) return EXIT;
		if (unit.eAI_IsChangingStance())
		return CONTINUE;
		if (unit.GetActionManager().GetRunningAction())
		{
			time += DeltaTime;
			if (time > timeout)  //! Looks like something went terribly wrong
			{
				EXTrace.Print(true, unit, "Bandaging_Self - timeout");
				unit.eAI_Unbug("bandage");
				time = 0;
				return EXIT;
			}
			return CONTINUE;
		}
		else
		{
			if (bandage)
			{
				if (unit.IsBleeding() && !bandage.IsDamageDestroyed())
				{
					last_bandage_attempt_time = GetGame().GetTime();
					time = 0;
					unit.StartActionObject(ActionBandageSelf, null);
					return CONTINUE;
				}
			}
		}
		if (unit.Expansion_GetUp(true))
		return CONTINUE;
		return EXIT;
	}
}
class Expansion_Master_PlayEmote_State_0: eAIState {
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_PlayEmote_State_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_PlayEmote_State_0";
		m_Name = "PlayEmote";
	}
	override void OnEntry(string Event, ExpansionState From) {
		unit.Expansion_PlayEmote();
	}
	override void OnExit(string Event, bool Aborted, ExpansionState To) {
	}
	override int OnUpdate(float DeltaTime, int SimulationPrecision) {
		return EXIT;
	}
}
class Expansion_Master__Unconscious_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Unconscious_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Unconscious_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Unconscious_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Unconscious_State_0"));
	}
	override int Guard() {
		if (!(unit.IsUnconscious())) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Unconscious_Idle_Transition_0: eAITransition {
	private Expansion_Master_Unconscious_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Unconscious_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Unconscious_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Unconscious_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		if (unit.IsUnconscious()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Interacting_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Interacting_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Interacting_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Interacting_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Interacting_State_0"));
	}
	override int Guard() {
		if (!(unit.eAI_HasInteractingPlayers())) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Interacting_Idle_Transition_0: eAITransition {
	private Expansion_Master_Interacting_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Interacting_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Interacting_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Interacting_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		if (unit.eAI_HasInteractingPlayers()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Bandaging_Self_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Bandaging_Self_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Bandaging_Self_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Bandaging_Self_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Bandaging_Self_State_0"));
	}
	override int Guard() {
		if (unit.IsFighting()) return FAIL;
		if (unit.IsRestrained()) return FAIL;
		if (!unit.IsBleeding()) return FAIL;
		if (GetGame().GetTime() - dst.last_bandage_attempt_time < 4000) return FAIL;
		auto hands = unit.GetItemInHands();
		if (!hands) return FAIL;
		if (!hands.Expansion_CanBeUsedToBandage() || hands.IsDamageDestroyed()) return FAIL;
		if (!unit.GetCommand_MoveAI()) return FAIL;
		dst.bandage = hands;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Bandaging_Self_Idle_Transition_0: eAITransition {
	private Expansion_Master_Bandaging_Self_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Bandaging_Self_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Bandaging_Self_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Bandaging_Self_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		if (unit.GetActionManager().GetRunningAction()) return FAIL;
		if (GetGame().GetTime() - src.last_bandage_attempt_time < 4000) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Weapon_Reloading_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Weapon_Reloading_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Weapon_Reloading_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Weapon_Reloading_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Weapon_Reloading_State_0"));
	}
	override int Guard() {
		if (GetGame().GetTime() - dst.sub_fsm.last_attempt_time < 1000) return FAIL;
		if (unit.IsClimbing() || unit.IsFalling() || unit.IsFighting() || !unit.GetCommand_MoveAI()) return FAIL;
		if (unit.IsRestrained()) return FAIL;
		if (!Class.CastTo(dst.sub_fsm.weapon, unit.GetItemInHands())) return FAIL;
		//! Allow sub-FSM to handle destroyed weapon so it gets dropped
		if (dst.sub_fsm.weapon.IsDamageDestroyed()) return SUCCESS;
		if (dst.sub_fsm.weapon.Expansion_IsChambered()) return FAIL;
		if (unit.GetWeaponManager().CanUnjam(dst.sub_fsm.weapon)) return FAIL;
		// don't move to the state if the action manager is operating
		if (!unit.GetActionManager() || unit.GetActionManager().GetRunningAction()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__TakeItemToHands_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_TakeItemToHands_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__TakeItemToHands_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__TakeItemToHands_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_TakeItemToHands_State_0"));
	}
	override int Guard() {
		if (unit.IsFighting()) return FAIL;
		if (unit.IsRestrained()) return FAIL;
		//! Taking items to hands while raised breaks hands! Wait until lowered
		if (unit.IsRaised()) return FAIL;
		ItemBase hands = unit.GetItemInHands();
		//! If ruined, drop
		if (hands && hands.IsDamageDestroyed())
		{
			unit.eAI_DropItem(hands);
			hands = null;
		}
		//! First check if we want to switch to bandage
		if (unit.IsBleeding() && (unit.GetThreatToSelf() < 0.4 || (unit.GetHealth01("", "Blood") < 0.7 && GetGame().GetTickTime() - unit.m_eAI_LastHitTime > 10)))
		{
			if (!hands || !hands.Expansion_CanBeUsedToBandage())
			{
				//! Item in hand is either not bandage/rag or is ruined
				dst.item = unit.GetBandageToUse();
				if (dst.item)
				{
					//! Try to put in inventory (shoulder slot or cargo), drop if not possible
					if (hands && !unit.eAI_TakeItemToInventory(hands))
					unit.eAI_DropItem(hands);
					return SUCCESS;
				}
			}
		}
		if (hands)
		return FAIL;
		dst.item = unit.GetWeaponToUse(true);
		if (dst.item)
		return SUCCESS;
		eAITarget target = unit.GetTarget();
		ItemBase targetItem;
		if (target && Class.CastTo(targetItem, target.GetEntity()) && (targetItem.IsWeapon() || targetItem.Expansion_IsMeleeWeapon()) && !targetItem.GetHierarchyRootPlayer() && !targetItem.IsSetForDeletion())
		{
			if (target.GetDistanceSq(unit, true) < 2.25 && target.GetThreat(unit) > 0.1)
			{
				dst.item = targetItem;
			}
		}
		if (dst.item)
		return SUCCESS;
		dst.item = unit.GetMeleeWeaponToUse();
		if (dst.item)
		return SUCCESS;
		return FAIL;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_TakeItemToHands_Idle_Transition_0: eAITransition {
	private Expansion_Master_TakeItemToHands_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_TakeItemToHands_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TakeItemToHands_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_TakeItemToHands_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__TakeItemToInventory_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_TakeItemToInventory_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__TakeItemToInventory_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__TakeItemToInventory_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_TakeItemToInventory_State_0"));
	}
	override int Guard() {
		if (unit.IsFighting()) return FAIL;
		if (unit.IsRestrained()) return FAIL;
		if (unit.IsRaised()) return FAIL;
		eAITarget target = unit.GetTarget();
		ItemBase targetItem;
		if (!target || !Class.CastTo(targetItem, target.GetEntity()) || targetItem.GetHierarchyRootPlayer() || targetItem.IsSetForDeletion())
		return FAIL;
		if (target.GetDistanceSq(unit, true) >= 2.25)
		return FAIL;
		if (targetItem.IsWeapon() || targetItem.IsMagazine())
		{
			//! If target is gun or magazine (latter means gun w/o ammo is in inventory) and we have melee in hand, prepare swap
			ItemBase hands = unit.GetItemInHands();
			if (hands && hands.Expansion_IsMeleeWeapon())
			{
				//! Only drop if destroyed, else might target it again...
				if (hands.IsDamageDestroyed())
				unit.eAI_DropItem(hands);
				else
				unit.eAI_TakeItemToInventory(hands);
			}
			if (targetItem.IsWeapon())  //! Picking up guns is handled by TakeItemToHands state
			return FAIL;
		}
		else if (targetItem.Expansion_IsMeleeWeapon())
		{
			return FAIL;
		}
		if (target.GetThreat(unit) <= 0.1)
		return FAIL;
		if (!unit.eAI_FindFreeInventoryLocationFor(targetItem))
		{
			unit.eAI_ItemThreatOverride(targetItem, true);
			return FAIL;
		}
		unit.eAI_ItemThreatOverride(targetItem, false);
		dst.item = targetItem;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_TakeItemToInventory_Idle_Transition_0: eAITransition {
	private Expansion_Master_TakeItemToInventory_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_TakeItemToInventory_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TakeItemToInventory_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_TakeItemToInventory_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Weapon_Unjamming_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Weapon_Unjamming_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Weapon_Unjamming_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Weapon_Unjamming_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Weapon_Unjamming_State_0"));
	}
	override int Guard() {
		if (unit.IsClimbing() || unit.IsFalling() || unit.IsFighting() || !unit.GetCommand_MoveAI()) return FAIL;
		if (unit.IsRestrained()) return FAIL;
		if (!Class.CastTo(dst.weapon, unit.GetItemInHands())) return FAIL;
		if (!unit.GetWeaponManager().CanUnjam(dst.weapon)) return FAIL;
		// don't move to the state if the action manager is operating
		if (!unit.GetActionManager() || unit.GetActionManager().GetRunningAction()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Weapon_Reloading_Idle_Transition_0: eAITransition {
	private Expansion_Master_Weapon_Reloading_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Weapon_Reloading_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Weapon_Reloading_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Weapon_Reloading_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Weapon_Unjamming_Idle_Transition_0: eAITransition {
	private Expansion_Master_Weapon_Unjamming_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Weapon_Unjamming_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Weapon_Unjamming_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Weapon_Unjamming_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Fighting_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Fighting_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Fighting_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Fighting_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Fighting_State_0"));
	}
	override int Guard() {
		if (unit.IsRestrained()) return FAIL;
		if (unit.GetThreatToSelf() < 0.4) return FAIL;
		if (unit.GetActionManager().GetRunningAction()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Fighting_Idle_Transition_0: eAITransition {
	private Expansion_Master_Fighting_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Fighting_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Fighting_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Fighting_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		if (unit.GetThreatToSelf() > 0.2) return FAIL;
		if (unit.IsFighting()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Vehicles_Idle_Transition_0: eAITransition {
	private Expansion_Master_Vehicles_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Vehicles_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Vehicles_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Vehicles_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		if (unit.IsInTransport()) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Vehicles_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Vehicles_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Vehicles_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Vehicles_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Vehicles_State_0"));
	}
	override int Guard() {
		auto group = unit.GetGroup();
		if (!group) return FAIL;
		if (group.GetFormationState() != eAIGroupFormationState.IN) return FAIL;
		auto leader = group.GetLeader();
		if (!leader || leader == unit) return FAIL;
		if (!leader.IsInTransport()) return FAIL;
		CarScript car;
		if (!Class.CastTo(car, leader.GetParent())) return FAIL;
		//TODO: make this event based instead and store as a variable within CarScript.
		//Prevents looping through the crew and insteads just compares a bool.
		for (int i = 1; i < car.CrewSize(); i++)
		{
			if (car.CrewMember(i) == null && !car.Expansion_IsSeatReservedByOther(i, unit) && car.IsAreaAtDoorFree(i))
			{
				dst.sub_fsm.seat = i;
				dst.sub_fsm.entity = car;
				car.Expansion_ReserveSeat(i, unit);
				return SUCCESS;
			}
		}
		return FAIL;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__PlayEmote_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_PlayEmote_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__PlayEmote_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__PlayEmote_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_PlayEmote_State_0"));
	}
	override int Guard() {
		if (unit.IsRestrained()) return FAIL;
		if (!unit.GetCommand_MoveAI()) return FAIL;
		if (unit.eAI_IsChangingStance()) return FAIL;
		if (!unit.m_Expansion_EmoteID) return FAIL;
		if (unit.GetEmoteManager().IsEmotePlaying() || unit.GetEmoteManager().Expansion_GetCurrentGesture() == unit.m_Expansion_EmoteID) return FAIL;
		if (unit.GetThreatToSelf(true) > 0.2) return FAIL;
		if (unit.IsFighting()) return FAIL;
		if (unit.GetWeaponManager().IsRunning()) return FAIL;
		if (unit.GetActionManager().GetRunningAction()) return FAIL;
		auto hands = unit.GetItemInHands();
		if (hands && hands.Expansion_CanBeUsedToBandage())
		return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_PlayEmote_Idle_Transition_0: eAITransition {
	private Expansion_Master_PlayEmote_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_PlayEmote_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_PlayEmote_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_PlayEmote_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Idle_FollowFormation_Transition_0: eAITransition {
	private Expansion_Master_Idle_State_0 src;
	private Expansion_Master_FollowFormation_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Idle_FollowFormation_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Idle_FollowFormation_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Idle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_FollowFormation_State_0"));
	}
	override int Guard() {
		if (unit.GetThreatToSelf() > 0.4) return FAIL;
		dst.group = unit.GetGroup();
		if (!dst.group) return FAIL;
		if (dst.group.GetFormationState() != eAIGroupFormationState.IN) return FAIL;
		auto leader = dst.group.GetLeader();
		if (!leader || leader == unit) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_FollowFormation_FollowFormation_Transition_0: eAITransition {
	private Expansion_Master_FollowFormation_State_0 src;
	private Expansion_Master_FollowFormation_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_FollowFormation_FollowFormation_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_FollowFormation_FollowFormation_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_FollowFormation_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_FollowFormation_State_0"));
	}
	override int Guard() {
		if (unit.GetThreatToSelf() > 0.4) return FAIL;
		dst.group = unit.GetGroup();
		if (!dst.group) return FAIL;
		if (dst.group.GetFormationState() != eAIGroupFormationState.IN) return FAIL;
		auto leader = dst.group.GetLeader();
		if (!leader || leader == unit) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_Idle_TraversingWaypoints_Transition_0: eAITransition {
	private Expansion_Master_Idle_State_0 src;
	private Expansion_Master_TraversingWaypoints_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_Idle_TraversingWaypoints_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_Idle_TraversingWaypoints_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_Idle_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_TraversingWaypoints_State_0"));
	}
	override int Guard() {
		if (unit.GetThreatToSelf() > 0.4) return FAIL;
		auto group = unit.GetGroup();
		if (!group) return FAIL;
		// we are the leader so we traverse the waypoints
		auto leader = group.GetLeader();
		if (leader && leader != unit) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_TraversingWaypoints_TraversingWaypoints_Transition_0: eAITransition {
	private Expansion_Master_TraversingWaypoints_State_0 src;
	private Expansion_Master_TraversingWaypoints_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_TraversingWaypoints_TraversingWaypoints_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TraversingWaypoints_TraversingWaypoints_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_TraversingWaypoints_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_TraversingWaypoints_State_0"));
	}
	override int Guard() {
		if (unit.GetThreatToSelf() > 0.4) return FAIL;
		auto group = unit.GetGroup();
		if (!group) return FAIL;
		// we are the leader so we traverse the waypoints
		auto leader = group.GetLeader();
		if (leader && leader != unit) return FAIL;
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_TraversingWaypoints_Idle_Transition_0: eAITransition {
	private Expansion_Master_TraversingWaypoints_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_TraversingWaypoints_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_TraversingWaypoints_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_TraversingWaypoints_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		auto group = unit.GetGroup();
		if (unit.GetThreatToSelf() > 0.4 || !group || group.GetLeader() != unit) return SUCCESS;
		return FAIL;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_FollowFormation_Idle_Transition_0: eAITransition {
	private Expansion_Master_FollowFormation_State_0 src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master_FollowFormation_Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master_FollowFormation_Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("Expansion_Master_FollowFormation_State_0"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		auto group = unit.GetGroup();
		if (!group || group.GetLeader() == unit || group.GetFormationState() != eAIGroupFormationState.IN) return SUCCESS;
		if (unit.GetThreatToSelf() > 0.4) return SUCCESS;
		return FAIL;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master__Idle_Transition_0: eAITransition {
	private ExpansionState src;
	private Expansion_Master_Idle_State_0 dst;
	Expansion_Master_FSM_0 fsm;
	void Expansion_Master__Idle_Transition_0(ExpansionFSM _fsm) {
		Class.CastTo(fsm, _fsm);
		m_ClassName = "Expansion_Master__Idle_Transition_0";
		Class.CastTo(src, _fsm.GetState("ExpansionState"));
		Class.CastTo(dst, _fsm.GetState("Expansion_Master_Idle_State_0"));
	}
	override int Guard() {
		return SUCCESS;
	}
	override ExpansionState GetSource() { return src; }
	override ExpansionState GetDestination() { return dst; }
	override string GetEvent() { return ""; }
}
class Expansion_Master_FSM_0: eAIFSM {
	void Expansion_Master_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
		m_Name = "Master";
		m_DefaultState = "Expansion_Master_Idle_State_0";
		Setup();
	}
	void Setup() {
		AddState(new Expansion_Master_Idle_State_0(this));
		AddState(new Expansion_Master_Unconscious_State_0(this));
		AddState(new Expansion_Master_Interacting_State_0(this));
		AddState(new Expansion_Master_FollowFormation_State_0(this));
		AddState(new Expansion_Master_TraversingWaypoints_State_0(this));
		AddState(new Expansion_Master_Vehicles_State_0(this));
		AddState(new Expansion_Master_Fighting_State_0(this));
		AddState(new Expansion_Master_Weapon_Reloading_State_0(this));
		AddState(new Expansion_Master_Weapon_Unjamming_State_0(this));
		AddState(new Expansion_Master_TakeItemToHands_State_0(this));
		AddState(new Expansion_Master_TakeItemToInventory_State_0(this));
		AddState(new Expansion_Master_Bandaging_Self_State_0(this));
		AddState(new Expansion_Master_PlayEmote_State_0(this));
		AddTransition(new Expansion_Master__Unconscious_Transition_0(this));
		AddTransition(new Expansion_Master_Unconscious_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Interacting_Transition_0(this));
		AddTransition(new Expansion_Master_Interacting_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Bandaging_Self_Transition_0(this));
		AddTransition(new Expansion_Master_Bandaging_Self_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Weapon_Reloading_Transition_0(this));
		AddTransition(new Expansion_Master__TakeItemToHands_Transition_0(this));
		AddTransition(new Expansion_Master_TakeItemToHands_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__TakeItemToInventory_Transition_0(this));
		AddTransition(new Expansion_Master_TakeItemToInventory_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Weapon_Unjamming_Transition_0(this));
		AddTransition(new Expansion_Master_Weapon_Reloading_Idle_Transition_0(this));
		AddTransition(new Expansion_Master_Weapon_Unjamming_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Fighting_Transition_0(this));
		AddTransition(new Expansion_Master_Fighting_Idle_Transition_0(this));
		AddTransition(new Expansion_Master_Vehicles_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Vehicles_Transition_0(this));
		AddTransition(new Expansion_Master__PlayEmote_Transition_0(this));
		AddTransition(new Expansion_Master_PlayEmote_Idle_Transition_0(this));
		AddTransition(new Expansion_Master_Idle_FollowFormation_Transition_0(this));
		AddTransition(new Expansion_Master_FollowFormation_FollowFormation_Transition_0(this));
		AddTransition(new Expansion_Master_Idle_TraversingWaypoints_Transition_0(this));
		AddTransition(new Expansion_Master_TraversingWaypoints_TraversingWaypoints_Transition_0(this));
		AddTransition(new Expansion_Master_TraversingWaypoints_Idle_Transition_0(this));
		AddTransition(new Expansion_Master_FollowFormation_Idle_Transition_0(this));
		AddTransition(new Expansion_Master__Idle_Transition_0(this));
	}
}
ExpansionFSM Create_Expansion_Master_FSM_0(ExpansionFSMOwnerType owner, ExpansionState parentState) {
	return new Expansion_Master_FSM_0(owner, parentState);
}
